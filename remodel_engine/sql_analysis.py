"""Static analysis helpers for dbt-style SQL (Jinja refs/sources + CTE structure)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

REF_PATTERN = re.compile(
    r"\{\{\s*ref\s*\(\s*['\"]([^'\"]+)['\"]\s*\)\s*\}\}",
    re.IGNORECASE,
)
SOURCE_PATTERN = re.compile(
    r"\{\{\s*source\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)\s*\}\}",
    re.IGNORECASE,
)

WINDOW_FUNCS = (
    "ROW_NUMBER",
    "RANK",
    "DENSE_RANK",
    "NTILE",
    "LAG",
    "LEAD",
    "FIRST_VALUE",
    "LAST_VALUE",
    "SUM",
)
WINDOW_PATTERN = re.compile(
    r"\b(" + "|".join(WINDOW_FUNCS[:9]) + r")\s*\(",
    re.IGNORECASE,
)
JOIN_PATTERN = re.compile(r"\b(?:INNER|LEFT|RIGHT|FULL|CROSS)?\s*JOIN\b", re.IGNORECASE)
GROUP_BY_PATTERN = re.compile(r"\bGROUP\s+BY\b", re.IGNORECASE)
AGG_PATTERN = re.compile(r"\b(SUM|COUNT|AVG|MIN|MAX)\s*\(", re.IGNORECASE)
CASE_PATTERN = re.compile(r"\bCASE\b", re.IGNORECASE)

CTE_BLOCK_PATTERN = re.compile(
    r"\bWITH\b(?P<body>.*?)(?=\bSELECT\b(?!\s*.*?\bFROM\b))",
    re.IGNORECASE | re.DOTALL,
)
CTE_NAME_PATTERN = re.compile(
    r"([a-zA-Z_][\w]*)\s+AS\s*\(",
    re.IGNORECASE,
)


@dataclass
class CteDefinition:
    name: str
    sql: str
    start: int
    end: int


@dataclass
class SqlAnalysis:
    refs: list[str] = field(default_factory=list)
    sources: list[tuple[str, str]] = field(default_factory=list)
    has_join: bool = False
    has_window: bool = False
    has_aggregation: bool = False
    has_case: bool = False
    ctes: list[CteDefinition] = field(default_factory=list)


def strip_jinja_comments(sql: str) -> str:
    sql = re.sub(r"\{#.*?#\}", "", sql, flags=re.DOTALL)
    sql = re.sub(r"\{\{.*?\}\}", " __JINJA__ ", sql, flags=re.DOTALL)
    return sql


def extract_refs(sql: str) -> list[str]:
    return REF_PATTERN.findall(sql)


def extract_sources(sql: str) -> list[tuple[str, str]]:
    return SOURCE_PATTERN.findall(sql)


def analyze_sql(sql: str) -> SqlAnalysis:
    bare = strip_jinja_comments(sql)
    return SqlAnalysis(
        refs=extract_refs(sql),
        sources=extract_sources(sql),
        has_join=bool(JOIN_PATTERN.search(bare)),
        has_window=bool(WINDOW_PATTERN.search(bare)),
        has_aggregation=bool(GROUP_BY_PATTERN.search(bare) or AGG_PATTERN.search(bare)),
        has_case=bool(CASE_PATTERN.search(bare)),
        ctes=parse_ctes(sql),
    )


def parse_ctes(sql: str) -> list[CteDefinition]:
    """Parse top-level WITH ... cte definitions (balanced parentheses)."""
    match = re.search(r"^\s*WITH\b", sql, re.IGNORECASE | re.MULTILINE)
    if not match:
        return []

    i = match.end()
    ctes: list[CteDefinition] = []
    while i < len(sql):
        while i < len(sql) and sql[i].isspace():
            i += 1
        name_match = re.match(r"([a-zA-Z_][\w]*)\s+AS\s*\(", sql[i:], re.IGNORECASE)
        if not name_match:
            break
        name = name_match.group(1)
        paren_start = i + name_match.end() - 1
        depth = 0
        j = paren_start
        while j < len(sql):
            ch = sql[j]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    body = sql[paren_start + 1 : j]
                    ctes.append(
                        CteDefinition(
                            name=name,
                            sql=body.strip(),
                            start=paren_start + 1,
                            end=j,
                        )
                    )
                    j += 1
                    while j < len(sql) and sql[j].isspace():
                        j += 1
                    if j < len(sql) and sql[j] == ",":
                        j += 1
                        i = j
                        break
                    i = j
                    break
            j += 1
        else:
            break
        if i >= len(sql) or not sql[i : i + 6].upper().startswith("SELECT"):
            if not (j < len(sql) and sql[j:].lstrip().upper().startswith("SELECT")):
                continue
            break
    return ctes


def cte_is_filter_or_projection_only(cte_sql: str) -> tuple[bool, str]:
    """Return (allowed_for_merge, reason)."""
    analysis = analyze_sql(cte_sql)
    if analysis.has_window:
        return False, "contains_window_function"
    if analysis.has_aggregation:
        return False, "contains_aggregation"
    if analysis.has_join:
        return False, "contains_join"
    if analysis.has_case:
        return False, "contains_case_branch"
    return True, "filter_or_projection_only"


def count_cte_consumers(full_sql: str, cte_name: str) -> int:
    """Count how many other CTE bodies reference cte_name."""
    ctes = parse_ctes(full_sql)
    if not ctes:
        return 0
    pattern = re.compile(rf"\b{re.escape(cte_name)}\b", re.IGNORECASE)
    count = 0
    for cte in ctes:
        if cte.name.lower() == cte_name.lower():
            continue
        if pattern.search(cte.sql):
            count += 1
    tail = full_sql.split(ctes[-1].name, 1)[-1] if ctes else full_sql
    if pattern.search(tail):
        count += 1
    return count


def cte_window_consumed_in_multiple_ways(full_sql: str, cte: CteDefinition) -> bool:
    """True when a window CTE is referenced by more than one downstream consumer."""
    if not analyze_sql(cte.sql).has_window:
        return False
    return count_cte_consumers(full_sql, cte.name) > 1


def compile_dbt_sql(
    sql: str,
    model_table_map: dict[str, str],
    source_table_map: dict[tuple[str, str], str],
) -> str:
    """Replace ref/source Jinja with DuckDB table names for parity execution."""

    def ref_repl(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in model_table_map:
            raise KeyError(f"Unknown ref model: {name}")
        return model_table_map[name]

    def source_repl(match: re.Match[str]) -> str:
        key = (match.group(1), match.group(2))
        if key not in source_table_map:
            raise KeyError(f"Unknown source: {key}")
        return source_table_map[key]

    out = REF_PATTERN.sub(ref_repl, sql)
    out = SOURCE_PATTERN.sub(source_repl, out)
    out = re.sub(r"\{\{.*?\}\}", "", out, flags=re.DOTALL)
    return out.strip()
