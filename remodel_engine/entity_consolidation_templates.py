"""Fixed-shape dbt SQL templates for entity consolidation (not a generic generator)."""

from __future__ import annotations

import re
from typing import Any

from remodel_engine.schema import EntityConsolidationSpec

_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def crosswalk_model_name(spec: EntityConsolidationSpec) -> str:
    return f"int_{spec.new_entity}__crosswalk"


def validate_entity_consolidation_spec(spec: EntityConsolidationSpec) -> None:
    """Raise ValueError when any identifier is not a safe SQL/dbt name."""
    for name in (
        spec.new_entity,
        spec.new_key_column,
        spec.timestamp_column,
        *spec.conflict_fields,
        *spec.old_tables,
        *spec.old_key_columns.values(),
    ):
        if not _IDENTIFIER.match(name):
            raise ValueError(f"invalid SQL identifier: {name!r}")


def _sql_str_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _cluster_mappings(clusters: list[dict[str, Any]]) -> list[tuple[str, str, str]]:
    mappings: list[tuple[str, str, str]] = []
    for cluster in clusters:
        new_key = str(cluster.get("new_key", ""))
        for row in cluster.get("rows") or []:
            mappings.append(
                (
                    str(row["old_key"]),
                    str(row["old_table"]),
                    new_key,
                )
            )
    return mappings


def render_crosswalk_sql(
    spec: EntityConsolidationSpec,
    clusters: list[dict[str, Any]],
) -> str:
    validate_entity_consolidation_spec(spec)
    mappings = _cluster_mappings(clusters)
    if mappings:
        value_rows = ",\n    ".join(
            f"({_sql_str_literal(ok)}, {_sql_str_literal(ot)}, {_sql_str_literal(nk)})"
            for ok, ot, nk in mappings
        )
        clustered_cte = f"""clustered AS (
  SELECT * FROM (
    VALUES
    {value_rows}
  ) AS v(old_key, old_table, new_key)
)"""
    else:
        clustered_cte = """clustered AS (
  SELECT
    CAST(NULL AS VARCHAR) AS old_key,
    CAST(NULL AS VARCHAR) AS old_table,
    CAST(NULL AS VARCHAR) AS new_key
  WHERE FALSE
)"""

    singleton_parts: list[str] = []
    for old_table in spec.old_tables:
        key_col = spec.old_key_columns[old_table]
        table_lit = _sql_str_literal(old_table)
        singleton_parts.append(
            f"""SELECT
    CAST(src.{key_col} AS VARCHAR) AS old_key,
    {table_lit} AS old_table,
    {table_lit} || ':' || CAST(src.{key_col} AS VARCHAR) AS new_key
  FROM {{{{ ref('{old_table}') }}}} AS src
  WHERE NOT EXISTS (
    SELECT 1
    FROM clustered AS c
    WHERE c.old_key = CAST(src.{key_col} AS VARCHAR)
      AND c.old_table = {table_lit}
  )"""
        )
    singleton_sql = "\n  UNION ALL\n  ".join(singleton_parts)
    return f"""-- entity consolidation crosswalk: {spec.new_entity}
WITH
{clustered_cte}
SELECT old_key, old_table, new_key FROM clustered
UNION ALL
{singleton_sql}
"""


def _distinct_expr(field: str) -> str:
    return (
        f"COUNT(DISTINCT COALESCE(CAST({field} AS VARCHAR), '__EC_NULL__'))"
    )


def _render_field_resolution_expr(field: str) -> str:
    return f"""CASE
    WHEN g.ec_row_cnt = 1 THEN (
      SELECT MIN(u.{field})
      FROM unified AS u
      WHERE u.new_key = g.new_key
    )
    WHEN COALESCE(s.ec_distinct_{field}, 0) = 0 THEN CAST(NULL AS VARCHAR)
    WHEN s.ec_distinct_{field} = 1 THEN (
      SELECT MIN(u.{field})
      FROM unified AS u
      WHERE u.new_key = g.new_key
    )
    WHEN g.ec_row_cnt > 1
      AND COALESCE(s.ec_distinct_{field}, 0) > 1
      AND g.ec_null_ts_cnt > 0 THEN CAST(NULL AS VARCHAR)
    WHEN COALESCE(am.ec_distinct_{field}_at_max, 0) > 1 THEN CAST(NULL AS VARCHAR)
    ELSE (
      SELECT MIN(u.{field})
      FROM unified AS u
      WHERE u.new_key = g.new_key
        AND u._ec_ts = g.ec_max_ts
    )
  END AS {field}"""


def _render_review_flag(spec: EntityConsolidationSpec) -> str:
    parts: list[str] = []
    for field in spec.conflict_fields:
        parts.append(
            f"(g.ec_row_cnt > 1 AND COALESCE(s.ec_distinct_{field}, 0) > 1 "
            f"AND COALESCE(am.ec_distinct_{field}_at_max, 0) > 1)"
        )
        parts.append(
            f"(g.ec_row_cnt > 1 AND COALESCE(s.ec_distinct_{field}, 0) > 1 "
            f"AND g.ec_null_ts_cnt > 0)"
        )
    if not parts:
        return "FALSE AS _survivorship_review"
    return f"({' OR '.join(parts)}) AS _survivorship_review"


def render_entity_sql(spec: EntityConsolidationSpec) -> str:
    validate_entity_consolidation_spec(spec)
    crosswalk = crosswalk_model_name(spec)
    unified_parts: list[str] = []
    for old_table in spec.old_tables:
        key_col = spec.old_key_columns[old_table]
        table_lit = _sql_str_literal(old_table)
        field_cols = ", ".join(f"src.{f}" for f in spec.conflict_fields)
        field_sql = f", {field_cols}" if field_cols else ""
        unified_parts.append(
            f"""SELECT
    cw.new_key,
    {table_lit} AS old_table,
    cw.old_key,
    TRY_CAST(src.{spec.timestamp_column} AS TIMESTAMP) AS _ec_ts
    {field_sql}
  FROM {{{{ ref('{crosswalk}') }}}} AS cw
  INNER JOIN {{{{ ref('{old_table}') }}}} AS src
    ON cw.old_table = {table_lit}
   AND cw.old_key = CAST(src.{key_col} AS VARCHAR)"""
        )
    unified_sql = "\n  UNION ALL\n  ".join(unified_parts)

    stats_fields = ",\n    ".join(
        f"{_distinct_expr(field)} AS ec_distinct_{field}"
        for field in spec.conflict_fields
    )
    at_max_fields = ",\n    ".join(
        f"{_distinct_expr(field)} AS ec_distinct_{field}_at_max"
        for field in spec.conflict_fields
    )
    field_exprs = ",\n    ".join(_render_field_resolution_expr(f) for f in spec.conflict_fields)
    review = _render_review_flag(spec)

    return f"""-- consolidated entity: {spec.new_entity}
WITH unified AS (
  {unified_sql}
),
grain AS (
  SELECT
    new_key,
    COUNT(*)::BIGINT AS ec_row_cnt,
    COUNT(*) FILTER (WHERE _ec_ts IS NULL)::BIGINT AS ec_null_ts_cnt,
    MAX(_ec_ts) AS ec_max_ts
  FROM unified
  GROUP BY new_key
),
stats AS (
  SELECT
    new_key,
    {stats_fields}
  FROM unified
  GROUP BY new_key
),
at_max AS (
  SELECT
    u.new_key,
    {at_max_fields}
  FROM unified AS u
  INNER JOIN grain AS g
    ON u.new_key = g.new_key
   AND u._ec_ts = g.ec_max_ts
  GROUP BY u.new_key
)
SELECT
  g.new_key AS {spec.new_key_column},
  {field_exprs},
  {review}
FROM grain AS g
LEFT JOIN stats AS s ON g.new_key = s.new_key
LEFT JOIN at_max AS am ON g.new_key = am.new_key
"""


def render_compat_view_sql(old_table: str, spec: EntityConsolidationSpec) -> str:
    validate_entity_consolidation_spec(spec)
    crosswalk = crosswalk_model_name(spec)
    key_col = spec.old_key_columns[old_table]
    return f"""-- compat view for retired table `{old_table}` → `{spec.new_entity}`
SELECT
  src.*,
  xwalk.new_key AS {spec.new_key_column}
FROM {{{{ ref('{old_table}') }}}} AS src
INNER JOIN {{{{ ref('{crosswalk}') }}}} AS xwalk
  ON CAST(src.{key_col} AS VARCHAR) = xwalk.old_key
 AND xwalk.old_table = '{old_table}'
"""


def render_survivorship_audit_sql(spec: EntityConsolidationSpec) -> str:
    validate_entity_consolidation_spec(spec)
    crosswalk = crosswalk_model_name(spec)
    unions: list[str] = []
    for old_table in spec.old_tables:
        key_col = spec.old_key_columns[old_table]
        ts_col = spec.timestamp_column
        conflict_cols = ", ".join(f"src.{f}" for f in spec.conflict_fields)
        conflict_cols_sql = f", {conflict_cols}" if conflict_cols else ""
        unions.append(
            f"""    SELECT
      CAST(src.{key_col} AS VARCHAR) AS old_key,
      '{old_table}' AS old_table,
      xwalk.new_key,
      src.{ts_col} AS {ts_col}
      {conflict_cols_sql}
    FROM {{{{ ref('{old_table}') }}}} AS src
    INNER JOIN {{{{ ref('{crosswalk}') }}}} AS xwalk
      ON CAST(src.{key_col} AS VARCHAR) = xwalk.old_key
     AND xwalk.old_table = '{old_table}'"""
        )
    body = "\n    UNION ALL\n".join(unions)
    return f"""-- survivorship audit (no physical deletes): {spec.new_entity}
-- Per-field resolution verdicts are stored on RemodeledModel.merge_audits for the
-- survivorship audit model only (not as SQL columns).
SELECT * FROM (
{body}
) AS _audit_sources
"""
