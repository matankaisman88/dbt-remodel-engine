"""Refactoring Rules Engine — Section 4 (CTE merge + lookup/window rewrite with safety gates)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from pydantic import BaseModel, Field

from remodel_engine.sql_analysis import (
    analyze_sql,
    cte_is_filter_or_projection_only,
    cte_window_consumed_in_multiple_ways,
    parse_ctes,
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

    partition = ", ".join(spec.partition_by_columns) or "1"
    window_expr = (
        f"ROW_NUMBER() OVER (PARTITION BY {partition} "
        f"ORDER BY {spec.order_by_column}) AS rn_{spec.lookup_alias}"
    )
    marker = f"-- LOOKUP:{spec.lookup_alias}"
    if marker not in sql and spec.lookup_alias not in sql:
        return RefactorResult(
            sql=sql,
            passthrough_reasons=[f"lookup rewrite: marker for {spec.lookup_alias} not found"],
        )

    rewritten = re.sub(
        rf"(?i)(SELECT\s+)",
        rf"\1{window_expr}, ",
        sql,
        count=1,
    )
    rewritten = re.sub(
        rf"(?i)\bJOIN\b.*?{re.escape(spec.lookup_alias)}",
        f"JOIN (SELECT * FROM lookup_{spec.lookup_alias} WHERE rn_{spec.lookup_alias} = 1) {spec.lookup_alias}",
        rewritten,
        count=1,
    )
    return RefactorResult(sql=rewritten, window_functions_applied=1)


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
