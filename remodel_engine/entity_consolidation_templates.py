"""Fixed-shape dbt SQL templates for entity consolidation (not a generic generator)."""

from __future__ import annotations

from remodel_engine.schema import EntityConsolidationSpec


def _crosswalk_model_name(spec: EntityConsolidationSpec) -> str:
    return f"int_{spec.new_entity}__crosswalk"


def _audit_model_name(spec: EntityConsolidationSpec) -> str:
    return f"int_{spec.new_entity}__survivorship_audit"


def render_crosswalk_sql(spec: EntityConsolidationSpec) -> str:
    unions: list[str] = []
    for old_table in spec.old_tables:
        key_col = spec.old_key_columns[old_table]
        unions.append(
            f"""    SELECT
      CAST({key_col} AS VARCHAR) AS old_key,
      '{old_table}' AS old_table,
      CAST({key_col} AS VARCHAR) AS new_key
    FROM {{{{ ref('{old_table}') }}}}"""
        )
    body = "\n    UNION ALL\n".join(unions)
    return f"""-- entity consolidation crosswalk: {spec.new_entity}
SELECT * FROM (
{body}
) AS _crosswalk
"""


def render_compat_view_sql(old_table: str, spec: EntityConsolidationSpec) -> str:
    crosswalk = _crosswalk_model_name(spec)
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
    crosswalk = _crosswalk_model_name(spec)
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
-- Engine attaches per-field resolution verdicts in merge_audits metadata.
SELECT * FROM (
{body}
) AS _audit_sources
"""
