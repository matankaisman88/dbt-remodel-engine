from remodel_engine.sql_analysis import compile_dbt_sql, strip_dbt_directives


def test_strip_dbt_config_block_multiline() -> None:
    sql = """
-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_type_a"
  )
}}
SELECT 1 AS id FROM {{ source('dbo', 'src_master_data') }}
"""
    stripped = strip_dbt_directives(sql)
    assert "{{ config" not in stripped.lower()
    assert "SELECT 1" in stripped
    compiled = compile_dbt_sql(
        sql,
        model_table_map={},
        source_table_map={("dbo", "src_master_data"): "src_master_data"},
    )
    assert "{{" not in compiled
    assert "src_master_data" in compiled


def test_compile_dbt_sql_replaces_session_vars() -> None:
    sql = """
SELECT
    base.*,
    {{ var('BatchId') }} AS load_batch_id
FROM some_table base
"""
    compiled = compile_dbt_sql(sql, model_table_map={}, source_table_map={})
    assert "1 AS load_batch_id" in compiled
    assert "var(" not in compiled


def test_compile_dbt_sql_strips_incremental_block() -> None:
    sql = """
SELECT id FROM t
{% if is_incremental() %}
WHERE id > (SELECT max(id) FROM {{ this }})
{% endif %}
"""
    compiled = compile_dbt_sql(sql, model_table_map={}, source_table_map={})
    assert "is_incremental" not in compiled
    assert "WHERE id >" not in compiled
    assert compiled.endswith("FROM t")
