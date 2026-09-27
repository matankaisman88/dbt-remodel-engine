"""Restore Informatica-style SELECT * shadowing when SQL is materialized as CTAS.

Inline queries may list `join.col AS col` before `base.*`; the star expansion shadows
earlier `col` outputs with `base.col`. DuckDB CTAS assigns unique names (e.g. col_1)
instead of shadowing, which breaks downstream COALESCE/expr semantics after physical
decomposition.
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


def fix_star_shadowing_for_ctas(sql: str) -> str:
    """Drop join-sourced columns that are shadowed by a trailing `base.*` in CTAS."""
    body = sql.strip()
    if not body or ".*" not in body:
        return sql

    star_match = _TRAILING_STAR.search(body)
    if not star_match:
        return sql
    star_alias = star_match.group("alias")

    from_match = _FROM_PRIMARY_ALIAS.search(body)
    if not from_match or from_match.group("alias").lower() != star_alias.lower():
        return sql

    select_start = re.search(r"\bSELECT\b", body, re.IGNORECASE)
    from_start = re.search(r"\bFROM\b", body, re.IGNORECASE)
    if not select_start or not from_start or from_start.start() <= select_start.end():
        return sql

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
        return sql

    new_select = "\n".join(kept)
    new_body = (
        body[: select_start.end()]
        + new_select
        + body[from_start.start() :]
    )
    return new_body if new_body.endswith("\n") else new_body + "\n"


def _star_table_references_column(select_list: str, star_alias: str, column: str) -> bool:
    """True when the star source table exposes `column` (explicit or via base.*)."""
    pattern = rf"\b{re.escape(star_alias)}\.{re.escape(column)}\b"
    return re.search(pattern, select_list, re.IGNORECASE) is not None
