"""Restore Informatica-style SELECT * shadowing when SQL is materialized as CTAS.

Inline queries may list ``join.col AS col`` before ``base.*``; Informatica treats the
star expansion as shadowing that join column with ``base.col``. DuckDB CTAS keeps both
(``col``, ``col_1``), which changes ``COALESCE(col_DIM, col)`` unless harmonized.

Trailing-star bind harmonization (``harmonize_bind_select_ast``) is a general CTAS rule.

Lookup rename + COALESCE expansion is manifest-driven via ``ShadowedLookupRenameSpec``
(see ``ShadowedLookupRenameSpec`` in ``remodel_engine/schema.py``). When no spec matches the model/SQL, those
rules are skipped; the trailing-star drop rule remains fully automatic.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

import sqlglot
from sqlglot import exp
from sqlglot.errors import ParseError

from remodel_engine.schema import ShadowedLookupRenameSpec

_JINJA_PLACEHOLDER = re.compile(r"\{\{[^}]+\}\}")


def fix_star_shadowing_for_ctas(
    sql: str,
    *,
    dialect: str = "duckdb",
    model_name: str | None = None,
    source_raw_model: str | None = None,
    shadowed_lookup_renames: Sequence[ShadowedLookupRenameSpec] = (),
    renamed_column_present: bool = False,
) -> str:
    """Harmonize star-shadowed join projections for DuckDB CTAS."""
    body = sql.strip()
    if not body:
        return sql

    model_specs = _shadow_specs_for_model(
        model_name,
        source_raw_model,
        shadowed_lookup_renames,
    )
    lookup_spec = _lookup_rename_spec_for_sql(body, model_specs)

    try:
        parse_sql, jinja_map = _jinja_to_parse_placeholders(body)
        ast = sqlglot.parse_one(parse_sql, read=dialect)
    except ParseError:
        return _ensure_trailing_newline(sql)

    changed = False
    if isinstance(ast, exp.Select):
        ast, harmonized = harmonize_bind_select_ast(ast, lookup_spec=lookup_spec)
        changed |= harmonized

    coalesce_spec: ShadowedLookupRenameSpec | None = None
    if renamed_column_present and model_specs:
        if len(model_specs) == 1:
            coalesce_spec = model_specs[0]
        else:
            upper_body = body.upper()
            for spec in model_specs:
                if spec.dim_column.upper() in upper_body:
                    coalesce_spec = spec
                    break

    ast, coalesce_changed = rewrite_coalesce_bindings_ast(
        ast,
        lookup_spec=coalesce_spec,
    )
    changed |= coalesce_changed

    if not changed:
        return _ensure_trailing_newline(sql)

    out = _restore_jinja_placeholders(ast.sql(dialect=dialect), jinja_map)
    return _ensure_trailing_newline(out)


def _shadow_specs_for_model(
    model_name: str | None,
    source_raw_model: str | None,
    specs: Sequence[ShadowedLookupRenameSpec],
) -> list[ShadowedLookupRenameSpec]:
    if not specs:
        return []
    matched: list[ShadowedLookupRenameSpec] = []
    for spec in specs:
        if model_name and (
            model_name == spec.model_name
            or model_name.startswith(f"int_{spec.model_name}__")
        ):
            matched.append(spec)
        elif source_raw_model == spec.model_name:
            matched.append(spec)
    return matched


def _lookup_rename_spec_for_sql(
    sql: str,
    model_specs: Sequence[ShadowedLookupRenameSpec],
) -> ShadowedLookupRenameSpec | None:
    for spec in model_specs:
        if re.search(spec.lookup_ref_pattern, sql, flags=re.IGNORECASE):
            return spec
    return None


def harmonize_bind_select_ast(
    select: exp.Select,
    *,
    lookup_spec: ShadowedLookupRenameSpec | None = None,
) -> tuple[exp.Select, bool]:
    """Rewrite bind SELECT projections for trailing ``base.*`` star shadowing."""
    star_alias = _trailing_star_alias(select)
    if not star_alias:
        return select, False

    primary_alias = _primary_from_alias(select)
    if not primary_alias or primary_alias.lower() != star_alias.lower():
        return select, False

    changed = False
    kept: list[exp.Expression] = []
    for expression in select.expressions:
        if isinstance(expression, exp.Alias):
            shadow = _shadow_candidate_alias(expression)
            if shadow is not None:
                table_alias, column_name, output_name = shadow
                if lookup_spec is not None:
                    if (
                        column_name.upper() == lookup_spec.base_column.upper()
                        and output_name.upper() == lookup_spec.base_column.upper()
                        and table_alias.lower() != "base"
                    ):
                        expression.set(
                            "alias",
                            exp.to_identifier(lookup_spec.renamed_column),
                        )
                        kept.append(expression)
                        changed = True
                        continue

                if (
                    table_alias.lower() != star_alias.lower()
                    and _select_references_column(select, star_alias, column_name)
                ):
                    changed = True
                    continue

        kept.append(expression)

    if changed:
        select.set("expressions", kept)
    return select, changed


def rewrite_coalesce_bindings_ast(
    root: exp.Expression,
    *,
    lookup_spec: ShadowedLookupRenameSpec | None = None,
) -> tuple[exp.Expression, bool]:
    """Expand ``COALESCE(dim, base)`` with manifest-configured shadowed lookup column."""
    if lookup_spec is None:
        return root, False

    changed = False

    def _transform(node: exp.Expression) -> exp.Expression:
        nonlocal changed
        if not isinstance(node, exp.Coalesce):
            return node

        dim = node.this
        if not isinstance(dim, exp.Column) or not dim.name:
            return node
        if dim.name.upper() != lookup_spec.dim_column.upper():
            return node

        args = list(node.expressions)
        if len(args) != 1 or not isinstance(args[0], exp.Column):
            return node
        pk = args[0]
        if pk.name.upper() != lookup_spec.base_column.upper():
            return node

        lkp = exp.column(lookup_spec.renamed_column)
        if pk.table:
            lkp.set("table", exp.to_identifier(pk.table))

        changed = True
        return exp.Coalesce(
            this=dim.copy(),
            expressions=[lkp, pk.copy()],
        )

    return root.transform(_transform, copy=True), changed


def _jinja_to_parse_placeholders(sql: str) -> tuple[str, dict[str, str]]:
    mapping: dict[str, str] = {}
    counter = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal counter
        key = f"__JINJA_{counter}__"
        mapping[key] = match.group(0)
        counter += 1
        return key

    return _JINJA_PLACEHOLDER.sub(repl, sql), mapping


def _restore_jinja_placeholders(sql: str, mapping: dict[str, str]) -> str:
    out = sql
    for key, original in mapping.items():
        out = out.replace(key, original)
    return out


def _ensure_trailing_newline(sql: str) -> str:
    if sql.endswith("\n"):
        return sql
    return sql + "\n"


def _primary_from_alias(select: exp.Select) -> str | None:
    from_clause = select.find(exp.From)
    if not from_clause or not isinstance(from_clause.this, exp.Table):
        return None
    return from_clause.this.alias_or_name


def _trailing_star_alias(select: exp.Select) -> str | None:
    if not select.expressions:
        return None
    last = select.expressions[-1]
    if not _is_qualified_star(last):
        return None
    assert isinstance(last, exp.Column)
    return last.table


def _is_qualified_star(expression: exp.Expression) -> bool:
    if isinstance(expression, exp.Column) and isinstance(expression.this, exp.Star):
        return bool(expression.table)
    return False


def _shadow_candidate_alias(
    alias: exp.Alias,
) -> tuple[str, str, str] | None:
    if not isinstance(alias.this, exp.Column):
        return None
    column = alias.this
    table_alias = column.table
    column_name = column.name
    output_name = alias.alias
    if not table_alias or not column_name or not output_name:
        return None
    if column_name.upper() != output_name.upper():
        return None
    return table_alias, column_name, output_name


def _select_references_column(
    select: exp.Select,
    table_alias: str,
    column: str,
) -> bool:
    target_table = table_alias.lower()
    target_column = column.upper()
    for expression in select.expressions:
        for node in expression.walk():
            if isinstance(node, exp.Column) and isinstance(node.this, exp.Identifier):
                if (
                    node.table
                    and node.table.lower() == target_table
                    and node.name
                    and node.name.upper() == target_column
                ):
                    return True
    return False
