"""Layered schema mapping and config sanitization."""

from pathlib import Path

from remodel_engine.layered_dbt_config import (
    layered_dbt_project_yml_text,
    sanitize_layered_model_sql,
    write_layered_dbt_project,
)
from remodel_engine.physical_decomposer import physical_decompose_batch

_MART_SQL = """
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_type_a"
  )
}}
WITH
    sq_sq_master_data AS (
SELECT ENTITY_ID FROM {{ source('dbo', 'src_master_data') }}
)
SELECT ENTITY_ID FROM sq_sq_master_data
"""


def test_sanitize_layered_model_sql_removes_schema_override() -> None:
    cleaned = sanitize_layered_model_sql(_MART_SQL)
    assert 'schema = "dbo"' not in cleaned.lower()
    assert "alias = " in cleaned
    assert "materialized" in cleaned


def test_physical_decompose_drops_schema_from_mart_config() -> None:
    result = physical_decompose_batch(
        [{"model_name": "tgt_type_a", "sql": _MART_SQL, "materialization": "table"}]
    )
    mart = next(m for m in result.models if m.is_mart)
    assert 'schema = "dbo"' not in mart.sql.lower()
    assert mart.relative_path.startswith("models/marts/")


def test_layered_dbt_project_yml_maps_folders_to_schemas() -> None:
    yml = layered_dbt_project_yml_text("informatica_xml_real_world_complex_pipeline")
    assert "informatica_xml_real_world_complex_pipeline:" in yml
    assert "staging:" in yml
    assert "+schema: staging" in yml
    assert "+schema: intermediate" in yml
    assert "+schema: marts" in yml


def test_write_layered_dbt_project(tmp_path: Path) -> None:
    path = write_layered_dbt_project(tmp_path, project_name="demo_pipeline")
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "name: demo_pipeline" in text
    assert "+schema: marts" in text
