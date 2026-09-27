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
VAR_PATTERN = re.compile(
    r"\{\{\s*var\s*\(\s*['\"]([^'\"]+)['\"]\s*(?:,\s*[^)]+)?\s*\)\s*\}\}",
    re.IGNORECASE,
)
_THIS_PATTERN = re.compile(r"\{\{\s*this\s*\}\}", re.IGNORECASE)
_IS_INCREMENTAL_BLOCK = re.compile(
    r"\{%\s*if\s+is_incremental\s*\(\s*\)\s*%\}.*?\{%\s*endif\s*%\}",
    re.DOTALL | re.IGNORECASE,
)

# Defaults aligned with etl_to_dbt_airflow dbt_project.yml parity seeds.
_PARITY_VAR_DEFAULTS: dict[str, str] = {
    "BatchId": "1",
    "LastDeltaWatermark": "1900-01-01",
}

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
_WINDOW_OVER_PATTERN = re.compile(
    r"\b(ROW_NUMBER|RANK|DENSE_RANK|NTILE|LAG|LEAD|FIRST_VALUE|LAST_VALUE)\s*\("
    r"[\s\S]*?\)\s*OVER\s*\(",
    re.IGNORECASE,
)
_RISKY_JOIN_PATTERN = re.compile(
    r"\b(?:FULL|RIGHT|CROSS)\s+(?:OUTER\s+)?JOIN\b",
    re.IGNORECASE,
)
_NON_EQUI_JOIN_ON_PATTERN = re.compile(
    r"\bJOIN\b[\s\S]{0,400}?\bON\b[\s\S]{0,400}?(?:\bOR\b|<>|!=|>|<|\bBETWEEN\b|\bLIKE\b)",
    re.IGNORECASE,
)
_DEDUP_RN_FILTER_PATTERN = re.compile(
    r"(?:\bQUALIFY\b[\s\S]{0,120}?\bRN\w*\s*=\s*1\b|\bWHERE\b[\s\S]{0,200}?\bRN\w*\s*=\s*1\b)",
    re.IGNORECASE,
)
_SUBQUERY_IN_CASE_PATTERN = re.compile(
    r"\bCASE\b[\s\S]*?\bWHEN\b[\s\S]*?\(\s*SELECT\b",
    re.IGNORECASE,
)
_EXPRESSION_FUNC_PATTERN = re.compile(
    r"\b(?:upper|lower|trim|coalesce|cast|substring|regexp|concat|nvl|nullif|ifnull|"
    r"to_char|to_date|replace|split_part|md5|hash)\s*\(",
    re.IGNORECASE,
)
_DBT_CONTROL = re.compile(r"\{%.*?%\}", re.DOTALL)

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
        has_window=bool(WINDOW_PATTERN.search(bare) or _WINDOW_OVER_PATTERN.search(bare)),
        has_aggregation=bool(GROUP_BY_PATTERN.search(bare) or AGG_PATTERN.search(bare)),
        has_case=bool(CASE_PATTERN.search(bare)),
        ctes=parse_ctes(sql),
    )


def is_ref_column_passthrough(sql: str) -> bool:
    """
    True when SQL only projects from a single ref() without expressions or grain-changing ops.

    Used to let mart target models fall through to rule #3 instead of rule #2.
    """
    analysis = analyze_sql(sql)
    if not analysis.refs or len(analysis.refs) > 1:
        return False
    if (
        analysis.has_join
        or analysis.has_window
        or analysis.has_case
        or has_risky_aggregation(sql)
    ):
        return False
    bare = strip_jinja_comments(sql)
    return not _EXPRESSION_FUNC_PATTERN.search(bare)


def max_case_nesting_depth(sql: str) -> int:
    """Maximum nested CASE depth (END closes one CASE)."""
    bare = strip_jinja_comments(sql).upper()
    depth = 0
    max_depth = 0
    idx = 0
    while idx < len(bare):
        if bare.startswith("CASE", idx) and (idx == 0 or not bare[idx - 1].isalnum()):
            depth += 1
            max_depth = max(max_depth, depth)
            idx += 4
            continue
        if bare.startswith("END", idx) and (idx == 0 or not bare[idx - 1].isalnum()):
            depth = max(0, depth - 1)
            idx += 3
            continue
        idx += 1
    return max_depth


def has_complex_case(sql: str) -> bool:
    bare = strip_jinja_comments(sql)
    if not CASE_PATTERN.search(bare):
        return False
    if max_case_nesting_depth(sql) > 3:
        return True
    return bool(_SUBQUERY_IN_CASE_PATTERN.search(bare))


def has_risky_join(sql: str) -> bool:
    bare = strip_jinja_comments(sql)
    if not JOIN_PATTERN.search(bare):
        return False
    if _RISKY_JOIN_PATTERN.search(bare):
        return True
    return bool(_NON_EQUI_JOIN_ON_PATTERN.search(bare))


def is_standard_dedup_window(sql: str) -> bool:
    bare = strip_jinja_comments(sql)
    upper = bare.upper()
    if "ROW_NUMBER" not in upper or not _WINDOW_OVER_PATTERN.search(bare):
        return False
    return bool(_DEDUP_RN_FILTER_PATTERN.search(bare))


def has_risky_window(sql: str) -> bool:
    bare = strip_jinja_comments(sql)
    if not _WINDOW_OVER_PATTERN.search(bare):
        return False
    upper = bare.upper()
    if is_standard_dedup_window(sql):
        other_ranking = any(
            token in upper
            for token in ("LAG(", "LEAD(", "NTILE(", "RANK(", "DENSE_RANK(")
        )
        return other_ranking
    return True


def has_risky_aggregation(sql: str) -> bool:
    bare = strip_jinja_comments(sql)
    return bool(GROUP_BY_PATTERN.search(bare))


def assess_grain_risk(sql: str) -> tuple[bool, str | None]:
    """
    Return (needs_manual_review, reason) for transforms that may change grain or row counts.
    """
    reasons: list[str] = []
    if has_risky_join(sql):
        reasons.append("non-standard join (FULL/RIGHT/CROSS, OR, inequality, or fuzzy predicate)")
    if has_complex_case(sql):
        reasons.append("complex CASE (deep nesting or subquery in WHEN/THEN)")
    if has_risky_window(sql):
        reasons.append("window function beyond standard ROW_NUMBER dedup (rn = 1)")
    if has_risky_aggregation(sql):
        reasons.append("aggregation or GROUP BY that may change grain")
    if not reasons:
        return False, None
    return True, "; ".join(reasons)


def rule2_transform_summary(sql: str, analysis: SqlAnalysis | None = None) -> str:
    """Human-readable summary of why SQL qualifies as intermediate under rule #2."""
    analysis = analysis or analyze_sql(sql)
    parts: list[str] = []
    if analysis.has_join and not has_risky_join(sql):
        parts.append("lookup join")
    elif analysis.has_join:
        parts.append("join")
    if analysis.has_window:
        parts.append("window" if has_risky_window(sql) else "dedup window")
    if analysis.has_aggregation and not has_risky_aggregation(sql):
        parts.append("scalar aggregation")
    elif analysis.has_aggregation:
        parts.append("aggregation")
    if analysis.has_case and not has_complex_case(sql):
        parts.append("CASE")
    elif analysis.has_case:
        parts.append("complex CASE")
    if not parts:
        parts.append("projection/filter/expression")
    return ", ".join(parts)


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


def _parity_var_sql_literal(var_name: str) -> str:
    if var_name in _PARITY_VAR_DEFAULTS:
        return _PARITY_VAR_DEFAULTS[var_name]
    lowered = var_name.lower()
    if "watermark" in lowered or lowered.endswith("date") or "timestamp" in lowered:
        return "1900-01-01"
    if lowered.endswith("id"):
        return "1"
    return "NULL"


def compile_dbt_sql(
    sql: str,
    model_table_map: dict[str, str],
    source_table_map: dict[tuple[str, str], str],
) -> str:
    """Replace ref/source Jinja with DuckDB table names for parity execution."""
    out = strip_dbt_directives(sql)

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

    def var_repl(match: re.Match[str]) -> str:
        return _parity_var_sql_literal(match.group(1))

    out = REF_PATTERN.sub(ref_repl, out)
    out = SOURCE_PATTERN.sub(source_repl, out)
    out = VAR_PATTERN.sub(var_repl, out)
    out = _IS_INCREMENTAL_BLOCK.sub("", out)
    out = _THIS_PATTERN.sub("__dbt_this__", out)
    out = _DBT_CONTROL.sub("", out)
    out = re.sub(r"\{\{.*?\}\}", "", out, flags=re.DOTALL)
    out = re.sub(r"\{#.*?#\}", "", out, flags=re.DOTALL)
    return out.strip()


def strip_dbt_directives(sql: str) -> str:
    """Remove dbt config blocks and banner comments before warehouse execution."""
    _header, body = split_dbt_header_and_body(sql)
    return body


def split_dbt_header_and_body(sql: str) -> tuple[str, str]:
    """Return ``(dbt header comments + config, executable SQL body)``."""
    lines = sql.splitlines()
    banner: list[str] = []
    idx = 0
    while idx < len(lines):
        stripped = lines[idx].strip()
        if stripped.startswith("--") or stripped == "":
            banner.append(lines[idx])
            idx += 1
            continue
        if stripped.startswith("-- AUTO-GENERATED") or stripped.startswith(
            "-- MANUAL_REVIEW_REQUIRED"
        ):
            idx += 1
            continue
        break
    rest = "\n".join(lines[idx:])
    config_end = _find_config_block_end(rest)
    if config_end is not None:
        config_block = rest[:config_end].strip()
        after = rest[config_end:].lstrip("\n")
        after_lines = after.splitlines()
        body_idx = 0
        while body_idx < len(after_lines):
            stripped = after_lines[body_idx].strip()
            if stripped.startswith("--") or stripped == "":
                body_idx += 1
                continue
            break
        body = "\n".join(after_lines[body_idx:]).strip()
        header_parts = [*banner]
        if config_block:
            header_parts.append(config_block)
        header = "\n".join(header_parts).strip()
        return header, body or sql.strip()

    header = "\n".join(banner).strip()
    return header, rest.strip() or sql.strip()


def _find_config_block_end(text: str) -> int | None:
    match = re.search(r"\{\{[\s\n]*config\s*\(", text, re.IGNORECASE)
    if not match:
        return None
    paren_start = match.end() - 1
    depth = 0
    for idx in range(paren_start, len(text)):
        ch = text[idx]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                j = idx + 1
                while j < len(text) and text[j].isspace():
                    j += 1
                if j + 1 < len(text) and text[j : j + 2] == "}}":
                    return j + 2
                return None
    return None
