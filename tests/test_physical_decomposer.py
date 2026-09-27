"""Tests for physical CTE → dbt model decomposition."""

from remodel_engine.physical_decomposer import physical_decompose_batch

_MULTI_TARGET_SQL = """
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_type_a"
  )
}}
WITH
    sq_sq_master_data AS (
SELECT ENTITY_ID, ENTITY_TYPE, VALUE FROM {{ source('dbo', 'src_master_data') }}
),
    int_rtr_type AS (
    SELECT
        *
    FROM sq_sq_master_data base
)
SELECT
    ENTITY_ID AS ENTITY_ID,
    ENTITY_TYPE AS ENTITY_TYPE,
    VALUE AS VALUE
FROM int_rtr_type
"""


def test_multi_target_deduplicates_shared_ctes() -> None:
    raw_models = [
        {"model_name": "tgt_type_a", "sql": _MULTI_TARGET_SQL, "materialization": "table"},
        {
            "model_name": "tgt_type_b",
            "sql": _MULTI_TARGET_SQL.replace("tgt_type_a", "tgt_type_b"),
            "materialization": "table",
        },
    ]
    result = physical_decompose_batch(raw_models)
    names = {m.model_name for m in result.models}
    assert "stg_master_data" in names
    assert "int_rtr_type" in names or any(name.startswith("int_rtr_type") for name in names)
    assert "fct_type_a" in names
    assert "fct_type_b" in names
    assert result.shared_models_extracted >= 1

    stg_models = [m for m in result.models if m.model_name.startswith("stg_")]
    assert len(stg_models) == 1
    assert "{{ source('dbo', 'src_master_data') }}" in stg_models[0].sql
    assert "sq_sq_master_data" not in stg_models[0].sql.lower()

    mart_a = next(m for m in result.models if m.model_name == "fct_type_a")
    assert "{{ ref(" in mart_a.sql
    assert mart_a.relative_path.startswith("models/marts/")
    assert mart_a.is_mart


def test_monolith_without_ctes_becomes_single_model() -> None:
    sql = "SELECT id FROM {{ source('dbo', 'customers') }}"
    result = physical_decompose_batch([{"model_name": "raw_customers", "sql": sql}])
    assert len(result.models) == 1
    assert result.models[0].model_name == "customers"
    assert result.models[0].relative_path.startswith("models/")
