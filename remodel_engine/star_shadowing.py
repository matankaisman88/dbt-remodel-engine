"""Restore Informatica-style SELECT * shadowing when SQL is materialized as CTAS.

Inline queries may list ``join.col AS col`` before ``base.*``; Informatica treats the
star expansion as shadowing that join column with ``base.col``. DuckDB CTAS keeps both
(``col``, ``col_1``), which changes ``COALESCE(col_DIM, col)`` unless harmonized.

Rate-plan lookups use ``COALESCE(RATE_PLAN_PK_DIM, RATE_PLAN_PK)`` where the second
argument must remain the lookup projection when ``base.RATE_PLAN_PK`` is null. Those
join columns are renamed to ``RATE_PLAN_PK_LKP`` and COALESCE is expanded to three
arguments. Other shadowed join columns are dropped so ``col`` resolves to ``base.col``.
"""

from __future__ import annotations

import re

_FROM_PRIMARY_ALIAS = re.compile(
    r"\bFROM\s+(?:\{\{\s*ref\s*\([^)]+\)\s*\}\}|"
    r"\{\{\s*source\s*\([^)]+\)\s*\}\}|[\w.\"]+)\s+"
    r"(?P<alias>[a-zA-Z_][\w]*)\b",
    re.IGNORECASE,
)
_TRAILING_STAR = re.compile(
    r",\s*(?P<alias>[a-zA-Z_][\w]*)\.\*\s*(?=\s+FROM\b)",
    re.IGNORECASE | re.DOTALL,
)
_SHADOW_CANDIDATE = re.compile(
    r"^\s*(?P<table>[a-zA-Z_][\w]*)\.(?P<col>[a-zA-Z_][\w]*)\s+AS\s+(?P<out>[a-zA-Z_][\w]*)\s*,?\s*$",
    re.IGNORECASE,
)
_COALESCE_DIM_PAIR = re.compile(
    r"COALESCE\(\s*(?P<dim>[A-Za-z_][\w]*_DIM)\s*,\s*(?P<pk>[A-Za-z_][\w]*)\s*\)",
    re.IGNORECASE,
)
_RATE_PLAN_LKP_REF = re.compile(r"\blkp_lkp_ref_dim_rate_plan\b", re.IGNORECASE)


def fix_star_shadowing_for_ctas(sql: str) -> str:
    """Harmonize star-shadowed join projections for DuckDB CTAS."""
    body = sql.strip()
    if not body:
        return sql

    if _RATE_PLAN_LKP_REF.search(body):
        body = _rename_rate_plan_lookup_projection(body)

    body = _drop_shadowed_join_columns(body)
    body = _expand_rate_plan_pk_coalesce(body)
    return body if body.endswith("\n") else body + "\n"


def _rename_rate_plan_lookup_projection(body: str) -> str:
    lines = body.splitlines()
    out: list[str] = []
    for line in lines:
        match = _SHADOW_CANDIDATE.match(line)
        if (
            match
            and match.group("col") == match.group("out") == "RATE_PLAN_PK"
            and match.group("table").lower() != "base"
        ):
            out.append(
                line.replace(
                    f"{match.group('table')}.RATE_PLAN_PK AS RATE_PLAN_PK",
                    f"{match.group('table')}.RATE_PLAN_PK AS RATE_PLAN_PK_LKP",
                )
            )
            continue
        out.append(line)
    return "\n".join(out)


def _drop_shadowed_join_columns(body: str) -> str:
    if ".*" not in body:
        return body

    star_match = _TRAILING_STAR.search(body)
    if not star_match:
        return body
    star_alias = star_match.group("alias")

    from_match = _FROM_PRIMARY_ALIAS.search(body)
    if not from_match or from_match.group("alias").lower() != star_alias.lower():
        return body

    select_start = re.search(r"\bSELECT\b", body, re.IGNORECASE)
    from_start = re.search(r"\bFROM\b", body, re.IGNORECASE)
    if not select_start or not from_start or from_start.start() <= select_start.end():
        return body

    select_list = body[select_start.end() : from_start.start()]
    lines = select_list.splitlines()
    kept: list[str] = []
    changed = False
    for line in lines:
        match = _SHADOW_CANDIDATE.match(line)
        if (
            match
            and match.group("table").lower() != star_alias.lower()
            and match.group("col") == match.group("out")
            and _star_table_references_column(
                select_list, star_alias, match.group("col")
            )
        ):
            changed = True
            continue
        kept.append(line)

    if not changed:
        return body

    new_select = "\n".join(kept)
    return (
        body[: select_start.end()]
        + new_select
        + body[from_start.start() :]
    )


def _expand_rate_plan_pk_coalesce(body: str) -> str:
    def repl(match: re.Match[str]) -> str:
        dim = match.group("dim")
        pk = match.group("pk")
        if dim.upper() != "RATE_PLAN_PK_DIM" or pk.upper() != "RATE_PLAN_PK":
            return match.group(0)
        return f"COALESCE({dim}, RATE_PLAN_PK_LKP, {pk})"

    return _COALESCE_DIM_PAIR.sub(repl, body)


def _star_table_references_column(select_list: str, star_alias: str, column: str) -> bool:
    pattern = rf"\b{re.escape(star_alias)}\.{re.escape(column)}\b"
    return re.search(pattern, select_list, re.IGNORECASE) is not None
