"""Refactoring Rules Engine — Section 4 (CTE merge + lookup/window rewrite with safety gates)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import sqlglot
from pydantic import BaseModel, Field
from sqlglot import exp
from sqlglot.errors import ParseError

from remodel_engine.sql_analysis import (
    analyze_sql,
    assess_grain_risk,
    cte_is_filter_or_projection_only,
    cte_window_consumed_in_multiple_ways,
    is_ref_column_passthrough,
    parse_ctes,
    rule2_transform_summary,
)
from remodel_engine.star_shadowing import (
    _jinja_to_parse_placeholders,
    _restore_jinja_placeholders,
)

_LOOKUP_PARSE_DIALECT = "duckdb"


@dataclass
class Rule2Assessment:
    layer_intermediate: bool
    needs_manual_review: bool
    classification_reason: str


def assess_rule2(sql: str) -> Rule2Assessment:
    """
    Rule #2 — intermediate models with ref() upstream.

    Low-risk joins, dedup windows, simple CASE, and ref projections pass as intermediate.
    Grain-changing or ambiguous transforms fail closed to manual review.
    """
    analysis = analyze_sql(sql)
    if not analysis.refs:
        return Rule2Assessment(
            layer_intermediate=False,
            needs_manual_review=False,
            classification_reason="rule #2: no ref() upstream",
        )

    if is_ref_column_passthrough(sql):
        return Rule2Assessment(
            layer_intermediate=False,
            needs_manual_review=False,
            classification_reason="rule #2: ref column passthrough (defer to mart rule or fail-closed)",
        )

    risky, risk_reason = assess_grain_risk(sql)
    if risky:
        return Rule2Assessment(
            layer_intermediate=False,
            needs_manual_review=True,
            classification_reason=f"rule #2 grain risk: {risk_reason}",
        )

    summary = rule2_transform_summary(sql, analysis)
    return Rule2Assessment(
        layer_intermediate=True,
        needs_manual_review=False,
        classification_reason=f"matched rule #2: ref() upstream with {summary}",
    )


class CteMergeAudit(BaseModel):
    cte_merged_from: list[str]
    reason: str
    verified_by_parity: bool = False


class LookupRewriteSpec(BaseModel):
    """Manifest-driven lookup → window rewrite (formal equivalence only)."""

    model_name: str
    lookup_alias: str
    order_by_column: str
    partition_by_columns: list[str] = Field(default_factory=list)
    match_policy: str = "single_match"  # only single_match is supported


@dataclass
class RefactorResult:
    sql: str
    ctes_collapsed: int = 0
    window_functions_applied: int = 0
    merge_audits: list[CteMergeAudit] = field(default_factory=list)
    blocked_merges: list[str] = field(default_factory=list)
    passthrough_reasons: list[str] = field(default_factory=list)


def collapse_eligible_ctes(sql: str, *, enabled: bool = True) -> RefactorResult:
    if not enabled:
        return RefactorResult(sql=sql)

    result = RefactorResult(sql=sql)
    changed = True
    while changed:
        changed = False
        ctes = parse_ctes(result.sql)
        if len(ctes) < 2:
            break
        for idx in range(len(ctes) - 1):
            parent = ctes[idx + 1]
            child = ctes[idx]
            if child.name.lower() not in parent.sql.lower():
                continue
            if cte_window_consumed_in_multiple_ways(result.sql, child):
                msg = (
                    f"forbidden merge: CTE '{child.name}' has window function "
                    "consumed by multiple downstream consumers"
                )
                result.blocked_merges.append(msg)
                continue
            child_analysis = analyze_sql(child.sql)
            if child_analysis.has_window and count_distinct_select_lists(parent.sql, child.name) > 1:
                msg = f"forbidden merge: window CTE '{child.name}' multi-consumer side effect"
                result.blocked_merges.append(msg)
                continue
            allowed, reason = cte_is_filter_or_projection_only(child.sql)
            if not allowed:
                result.blocked_merges.append(
                    f"skipped merge for '{child.name}': not filter/projection-only ({reason})"
                )
                continue
            merged = _inline_cte(result.sql, child, parent)
            if merged != result.sql:
                result.sql = merged
                result.ctes_collapsed += 1
                result.merge_audits.append(
                    CteMergeAudit(
                        cte_merged_from=[child.name, parent.name],
                        reason=f"collapsed filter/projection CTE '{child.name}' into '{parent.name}'",
                        verified_by_parity=False,
                    )
                )
                changed = True
                break
    return result


def apply_lookup_window_rewrite(
    sql: str,
    spec: LookupRewriteSpec | None,
    *,
    enabled: bool = True,
) -> RefactorResult:
    if not enabled or spec is None:
        return RefactorResult(sql=sql)

    if spec.match_policy != "single_match":
        return RefactorResult(
            sql=sql,
            passthrough_reasons=[
                f"lookup rewrite fail-closed: ambiguous match_policy={spec.match_policy!r}"
            ],
        )

    body = sql.strip()
    if not body:
        return RefactorResult(sql=sql)

    marker = f"-- LOOKUP:{spec.lookup_alias}"
    try:
        parse_sql, jinja_map = _jinja_to_parse_placeholders(body)
        ast = sqlglot.parse_one(parse_sql, read=_LOOKUP_PARSE_DIALECT)
    except ParseError:
        return RefactorResult(
            sql=sql,
            passthrough_reasons=["lookup rewrite: sql parse failed"],
        )

    matching_joins = _lookup_joins_for_alias(ast, spec.lookup_alias)
    if not matching_joins:
        if marker not in sql and not _sql_references_lookup_alias(sql, spec.lookup_alias):
            return RefactorResult(
                sql=sql,
                passthrough_reasons=[f"lookup rewrite: marker for {spec.lookup_alias} not found"],
            )
        return RefactorResult(
            sql=sql,
            passthrough_reasons=[
                f"lookup rewrite: join with alias {spec.lookup_alias!r} not found"
            ],
        )

    if len(matching_joins) > 1:
        return RefactorResult(
            sql=sql,
            passthrough_reasons=[
                f"lookup rewrite fail-closed: multiple JOIN targets for alias {spec.lookup_alias!r}"
            ],
        )

    join = matching_joins[0]
    try:
        wrapped = _wrap_lookup_join_target(join.this, spec)
    except ParseError:
        return RefactorResult(
            sql=sql,
            passthrough_reasons=["lookup rewrite: failed to build wrapped lookup subquery"],
        )
    join.set("this", wrapped)

    out = _restore_jinja_placeholders(ast.sql(dialect=_LOOKUP_PARSE_DIALECT), jinja_map)
    if not out.endswith("\n") and sql.endswith("\n"):
        out += "\n"
    return RefactorResult(sql=out, window_functions_applied=1)


def _sql_references_lookup_alias(sql: str, lookup_alias: str) -> bool:
    """True when the alias appears as a lookup marker companion, not as a substring."""
    if re.search(rf"(?i)\bAS\s+{re.escape(lookup_alias)}\b", sql):
        return True
    if re.search(rf"(?i)\bJOIN\s+[^\n]+?\s{re.escape(lookup_alias)}\s+ON\b", sql):
        return True
    return False


def _lookup_joins_for_alias(root: exp.Expression, lookup_alias: str) -> list[exp.Join]:
    target = lookup_alias.lower()
    matches: list[exp.Join] = []
    for join in root.find_all(exp.Join):
        alias = join.this.alias
        if alias and alias.lower() == target:
            matches.append(join)
    return matches


def _wrap_lookup_join_target(
    join_target: exp.Expression,
    spec: LookupRewriteSpec,
) -> exp.Subquery:
    source = _lookup_source_from_join_target(join_target)
    partition = ", ".join(spec.partition_by_columns) or "1"
    rn_name = f"rn_{spec.lookup_alias}"
    alias = spec.lookup_alias
    scaffold = (
        f"SELECT _placeholder FROM ("
        f"SELECT * FROM ("
        f"SELECT *, ROW_NUMBER() OVER (PARTITION BY {partition} "
        f"ORDER BY {spec.order_by_column}) AS {rn_name} "
        f"FROM {source}"
        f") AS _lkp_wrapped WHERE {rn_name} = 1"
        f") AS {alias}"
    )
    parsed = sqlglot.parse_one(scaffold, read=_LOOKUP_PARSE_DIALECT)
    from_clause = parsed.find(exp.From)
    if not from_clause or not isinstance(from_clause.this, exp.Subquery):
        raise ParseError("expected wrapped lookup subquery")
    return from_clause.this


def _lookup_source_from_join_target(join_target: exp.Expression) -> str:
    if isinstance(join_target, exp.Table):
        return join_target.name
    if isinstance(join_target, exp.Subquery):
        return f"({join_target.this.sql(dialect=_LOOKUP_PARSE_DIALECT)})"
    return join_target.sql(dialect=_LOOKUP_PARSE_DIALECT)


def count_distinct_select_lists(parent_sql: str, child_name: str) -> int:
    """Heuristic: count SELECT fragments referencing child_name outside its definition."""
    parts = re.split(rf"\b{re.escape(child_name)}\b", parent_sql, flags=re.IGNORECASE)
    return max(1, len(parts) - 1)


def _inline_cte(full_sql: str, child, parent) -> str:
    """Replace references to child CTE in parent body with subquery."""
    ctes = parse_ctes(full_sql)
    if not ctes:
        return full_sql

    subquery = f"(\n{child.sql}\n)"
    new_parent_sql = re.sub(
        rf"\b{re.escape(child.name)}\b",
        subquery,
        parent.sql,
        flags=re.IGNORECASE,
    )

    rebuilt: list[str] = ["WITH"]
    for cte in ctes:
        if cte.name.lower() == child.name.lower():
            continue
        body = new_parent_sql if cte.name.lower() == parent.name.lower() else cte.sql
        rebuilt.append(f"{cte.name} AS (\n{body}\n)")
    with_clause = "WITH " + ",\n".join(rebuilt[1:])
    final_select_match = re.search(
        r"\bWITH\b[\s\S]*?\)\s*(SELECT[\s\S]+)\s*$",
        full_sql,
        re.IGNORECASE,
    )
    tail = (
        final_select_match.group(1).strip()
        if final_select_match
        else f"SELECT * FROM {parent.name}"
    )
    return f"{with_clause}\n{tail}"


def explain_gate(sql: str, conn) -> tuple[bool, str]:
    """DuckDB EXPLAIN — necessary but not sufficient (Section 4)."""
    try:
        conn.execute(f"EXPLAIN {sql}")
        return True, "explain_ok"
    except Exception as exc:  # noqa: BLE001 — surfaced in API response
        return False, str(exc)
