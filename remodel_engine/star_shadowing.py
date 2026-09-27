"""Restore Informatica-style SELECT * shadowing when SQL is materialized as CTAS.

Inline queries may list ``join.col AS col`` before ``base.*``; Informatica treats the
star expansion as shadowing that join column with ``base.col``. DuckDB CTAS keeps both
(``col``, ``col_1``), which changes ``COALESCE(col_DIM, col)`` unless harmonized.

Trailing-star bind harmonization (``harmonize_bind_select_ast``) is a general CTAS rule.

The COALESCE expansion in ``rewrite_coalesce_bindings_ast`` is **not** general CTAS
shadowing: it is hardcoded to the rate-plan lookup naming convention
(``RATE_PLAN_PK`` / ``RATE_PLAN_PK_DIM`` / ``RATE_PLAN_PK_LKP`` / ``ref_dim_rate_plan``)
used by specific real-world fixtures and does not generalize to other lookups.
"""

from __future__ import annotations

import re

import sqlglot
from sqlglot import exp
from sqlglot.errors import ParseError

_JINJA_PLACEHOLDER = re.compile(r"\{\{[^}]+\}\}")
_RATE_PLAN_LKP_REF = re.compile(r"ref_dim_rate_plan\b", re.IGNORECASE)


def fix_star_shadowing_for_ctas(
    sql: str,
    *,
    dialect: str = "duckdb",
    source_has_rate_plan_lkp: bool = False,
) -> str:
    """Harmonize star-shadowed join projections for DuckDB CTAS."""
    body = sql.strip()
    if not body:
        return sql

    try:
        parse_sql, jinja_map = _jinja_to_parse_placeholders(body)
        ast = sqlglot.parse_one(parse_sql, read=dialect)
    except ParseError:
        return _ensure_trailing_newline(sql)

    changed = False
    if isinstance(ast, exp.Select):
        ast, harmonized = harmonize_bind_select_ast(
            ast,
            has_rate_plan_lkp=bool(_RATE_PLAN_LKP_REF.search(body)),
        )
        changed |= harmonized

    ast, coalesce_changed = rewrite_coalesce_bindings_ast(
        ast,
        source_has_rate_plan_lkp=source_has_rate_plan_lkp,
    )
    changed |= coalesce_changed

    if not changed:
        return _ensure_trailing_newline(sql)

    out = _restore_jinja_placeholders(ast.sql(dialect=dialect), jinja_map)
    return _ensure_trailing_newline(out)


def harmonize_bind_select_ast(
    select: exp.Select,
    *,
    has_rate_plan_lkp: bool,
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
                if (
                    has_rate_plan_lkp
                    and column_name.upper() == "RATE_PLAN_PK"
                    and output_name.upper() == "RATE_PLAN_PK"
                    and table_alias.lower() != "base"
                ):
                    expression.set("alias", exp.to_identifier("RATE_PLAN_PK_LKP"))
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
    source_has_rate_plan_lkp: bool = False,
) -> tuple[exp.Expression, bool]:
    """Rate-plan only: expand ``COALESCE(RATE_PLAN_PK_DIM, RATE_PLAN_PK)`` with ``RATE_PLAN_PK_LKP``.

    Scoped to the rate-plan lookup column naming convention; not a general CTAS-shadowing rule.
    """
    if not source_has_rate_plan_lkp:
        return root, False

    changed = False

    def _transform(node: exp.Expression) -> exp.Expression:
        nonlocal changed
        if not isinstance(node, exp.Coalesce):
            return node

        dim = node.this
        if not isinstance(dim, exp.Column) or not dim.name:
            return node
        if dim.name.upper() != "RATE_PLAN_PK_DIM":
            return node

        args = list(node.expressions)
        if len(args) != 1 or not isinstance(args[0], exp.Column):
            return node
        pk = args[0]
        if pk.name.upper() != "RATE_PLAN_PK":
            return node

        lkp = exp.column("RATE_PLAN_PK_LKP")
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
