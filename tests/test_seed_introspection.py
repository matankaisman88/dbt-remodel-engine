"""Tests for seed SQL introspection."""

from remodel_engine.seed_introspection import extract_source_table_map


def test_extract_source_table_map_unquoted_schema_table() -> None:
    seeds = """
CREATE TABLE IF NOT EXISTS dbo.src_orders(ORDER_ID INTEGER);
CREATE TABLE IF NOT EXISTS legacy_ops_tmp.staging_raw_events(K VARCHAR);
"""
    assert extract_source_table_map(seeds) == {
        ("dbo", "src_orders"): "dbo.src_orders",
        ("legacy_ops_tmp", "staging_raw_events"): "legacy_ops_tmp.staging_raw_events",
    }


def test_extract_source_table_map_quoted_table_name() -> None:
    seeds = 'CREATE TABLE IF NOT EXISTS dbo."value"("VALUE" DOUBLE, ID INTEGER);'
    assert extract_source_table_map(seeds) == {("dbo", "value"): "dbo.value"}
