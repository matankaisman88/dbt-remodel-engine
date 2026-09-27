"""Derive parity metadata from DuckDB seed SQL."""

from __future__ import annotations

import re

_CREATE_TABLE = re.compile(
    r"\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?",
    re.IGNORECASE,
)
_UNQUOTED_IDENT = re.compile(r"[\w$]+")


def _parse_sql_identifier(sql: str, pos: int) -> tuple[str, int] | None:
    while pos < len(sql) and sql[pos].isspace():
        pos += 1
    if pos >= len(sql):
        return None
    if sql[pos] == '"':
        end = sql.find('"', pos + 1)
        if end == -1:
            return None
        return sql[pos + 1 : end], end + 1
    match = _UNQUOTED_IDENT.match(sql, pos)
    if not match:
        return None
    return match.group(0), match.end()


def _parse_qualified_table_name(sql: str, pos: int) -> tuple[str, str] | None:
    first = _parse_sql_identifier(sql, pos)
    if first is None:
        return None
    schema, pos = first
    while pos < len(sql) and sql[pos].isspace():
        pos += 1
    if pos >= len(sql) or sql[pos] != ".":
        return None
    pos += 1
    second = _parse_sql_identifier(sql, pos)
    if second is None:
        return None
    table, pos = second
    while pos < len(sql) and sql[pos].isspace():
        pos += 1
    if pos >= len(sql) or sql[pos] != "(":
        return None
    return schema, table


def extract_source_table_map(seeds_sql: str) -> dict[tuple[str, str], str]:
    """Map each CREATE TABLE schema.table to its DuckDB name (identity mapping)."""
    result: dict[tuple[str, str], str] = {}
    for match in _CREATE_TABLE.finditer(seeds_sql):
        qualified = _parse_qualified_table_name(seeds_sql, match.end())
        if qualified is None:
            continue
        schema, table = qualified
        result[(schema, table)] = f"{schema}.{table}"
    return result
