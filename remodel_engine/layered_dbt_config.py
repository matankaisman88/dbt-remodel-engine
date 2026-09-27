"""Layered dbt project defaults: folder → schema mapping and config sanitization."""

from __future__ import annotations

import re
from pathlib import Path

from remodel_engine.sql_analysis import split_dbt_header_and_body

_LAYER_SCHEMAS: dict[str, str] = {
    "staging": "staging",
    "intermediate": "intermediate",
    "marts": "marts",
}

_CONFIG_BLOCK_RE = re.compile(
    r"(\{\{\s*config\s*\([\s\S]*?\)\s*\}\})",
    re.IGNORECASE,
)
_SCHEMA_OPTION_RE = re.compile(
    r",?\s*schema\s*=\s*(?:\"[^\"]*\"|'[^']*')",
    re.IGNORECASE,
)
_SCHEMA_OPTION_LEADING_RE = re.compile(
    r"schema\s*=\s*(?:\"[^\"]*\"|'[^']*')\s*,\s*",
    re.IGNORECASE,
)


def sanitize_layered_model_sql(sql: str) -> str:
    """Drop per-model ``schema`` overrides; layered folders set schema via ``dbt_project.yml``."""
    header, body = split_dbt_header_and_body(sql)
    if not header:
        return sql
    sanitized_header = _strip_schema_from_header(header)
    if sanitized_header == header:
        return sql
    parts = [sanitized_header.strip()] if sanitized_header.strip() else []
    if body.strip():
        parts.append(body.strip())
    return "\n\n".join(parts) + ("\n" if sql.endswith("\n") else "")


def _strip_schema_from_header(header: str) -> str:
    def _clean_config_block(match: re.Match[str]) -> str:
        block = match.group(1)
        cleaned = _SCHEMA_OPTION_LEADING_RE.sub("", block)
        cleaned = _SCHEMA_OPTION_RE.sub("", cleaned)
        cleaned = re.sub(r",\s*,", ",", cleaned)
        cleaned = re.sub(r"\(\s*,", "(", cleaned)
        return cleaned

    return _CONFIG_BLOCK_RE.sub(_clean_config_block, header)


def layered_dbt_project_yml_text(
    project_name: str,
    *,
    profile: str = "etl_to_dbt_airflow",
) -> str:
    """Render ``dbt_project.yml`` with ``+schema`` per layered model subdirectory."""
    safe_name = project_name.strip() or "remodeled_project"
    lines = [
        f"name: {safe_name}",
        'version: "1.0.0"',
        "config-version: 2",
        f"profile: {profile}",
        "",
        'model-paths: ["models"]',
        'macro-paths: ["macros"]',
        'target-path: "/tmp/dbt_target"',
        'clean-targets: ["/tmp/dbt_target", "dbt_packages"]',
        "",
        "vars:",
        '  LastDeltaWatermark: "1900-01-01"',
        "  BatchId: 1",
        "",
        "models:",
        f"  {safe_name}:",
    ]
    for folder, schema in _LAYER_SCHEMAS.items():
        lines.append(f"    {folder}:")
        lines.append(f"      +schema: {schema}")
    lines.append("")
    return "\n".join(lines)


def write_layered_dbt_project(
    corpus_root: Path,
    *,
    project_name: str,
    profile: str = "etl_to_dbt_airflow",
) -> Path:
    dest = corpus_root / "dbt_project.yml"
    dest.write_text(
        layered_dbt_project_yml_text(project_name, profile=profile),
        encoding="utf-8",
    )
    return dest
