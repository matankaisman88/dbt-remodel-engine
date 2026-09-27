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
