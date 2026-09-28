"""DuckDB execution tests for entity consolidation SQL (not status-only)."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import duckdb
import pytest

from remodel_engine.engine import RemodelEngine
from remodel_engine.entity_consolidation import (
    execute_entity_consolidation_sql,
    rows_by_old_table,
)
from remodel_engine.entity_consolidation_templates import (
    render_crosswalk_sql,
    validate_entity_consolidation_spec,
)
from remodel_engine.grain_resolution import classify_and_resolve
from remodel_engine.schema import EntityConsolidationSpec
from remodel_engine.entity_consolidation import _source_record_from_dict

FEBRL_FIXTURE = (
    Path(__file__).parent / "fixtures" / "entity_consolidation" / "febrl_conflict_sample.json"
)


def _demo_spec(**overrides) -> EntityConsolidationSpec:
    base = dict(
        new_entity="dim_customer",
        old_tables=["legacy_cust_a", "legacy_cust_b"],
        old_key_columns={
            "legacy_cust_a": "cust_id",
            "legacy_cust_b": "cust_id",
        },
        new_key_column="customer_key",
        timestamp_column="updated_at",
        conflict_fields=["customer_name", "city"],
    )
    base.update(overrides)
    return EntityConsolidationSpec(**base)


def _merge_clusters() -> list[dict]:
    return [
        {
            "new_key": "cust-100",
            "rows": [
                {
                    "old_key": "1",
                    "old_table": "legacy_cust_a",
                    "timestamp": "2020-01-01T00:00:00",
                    "field_values": {
                        "customer_name": "Alice",
                        "city": "NY",
                        "updated_at": "2020-01-01",
                    },
                },
                {
                    "old_key": "2",
                    "old_table": "legacy_cust_b",
                    "timestamp": "2022-01-01T00:00:00",
                    "field_values": {
                        "customer_name": "Alicia",
                        "city": "NY",
                        "updated_at": "2022-01-01",
                    },
                },
            ],
        }
    ]


def _fetch_table(conn, table: str) -> list[dict]:
    cols = [r[0] for r in conn.execute(f"DESCRIBE {table}").fetchall()]
    rows = conn.execute(f"SELECT * FROM {table}").fetchall()
    return [dict(zip(cols, row, strict=True)) for row in rows]


def _run_spec(spec: EntityConsolidationSpec, clusters: list[dict], extra=None):
    conn = duckdb.connect(":memory:")
    executed = execute_entity_consolidation_sql(
        conn, spec, clusters, extra_rows=extra
    )
    return conn, executed


def test_merge_crosswalk_maps_both_sources_to_cluster_new_key():
    spec = _demo_spec()
    clusters = _merge_clusters()
    sql = render_crosswalk_sql(spec, clusters)
    assert "cust-100" in sql
    assert "CAST(cust_id AS VARCHAR) AS new_key" not in sql.replace(" ", "")

    conn, executed = _run_spec(spec, clusters)
    crosswalk = _fetch_table(conn, executed["int_dim_customer__crosswalk"])
    keys = {
        (r["old_table"], r["old_key"]): r["new_key"]
        for r in crosswalk
    }
    assert keys[("legacy_cust_a", "1")] == "cust-100"
    assert keys[("legacy_cust_b", "2")] == "cust-100"

    entity = _fetch_table(conn, executed["dim_customer"])
    cust100 = next(r for r in entity if r["customer_key"] == "cust-100")
    assert cust100["customer_name"] == "Alicia"
    assert len([r for r in entity if r["customer_key"] == "cust-100"]) == 1


def test_hand_modified_cluster_changes_crosswalk_and_entity():
    spec = _demo_spec()
    clusters = _merge_clusters()
    conn, executed = _run_spec(spec, clusters)
    before = _fetch_table(conn, executed["dim_customer"])

    modified = copy.deepcopy(clusters)
    modified[0]["new_key"] = "cust-999"
    conn2, executed2 = _run_spec(spec, modified)
    after = _fetch_table(conn2, executed2["dim_customer"])

    assert before != after
    assert any(r["customer_key"] == "cust-999" for r in after)
    assert not any(r["customer_key"] == "cust-100" for r in after)


def test_singleton_fallback_retains_unclustered_row():
    spec = _demo_spec()
    clusters = _merge_clusters()
    extra = [
        {
            "old_key": "orphan-7",
            "old_table": "legacy_cust_a",
            "timestamp": "2019-01-01T00:00:00",
            "field_values": {
                "customer_name": "Solo",
                "city": "TX",
                "updated_at": "2019-01-01",
            },
        }
    ]
    conn, executed = _run_spec(spec, clusters, extra=extra)
    crosswalk = _fetch_table(conn, executed["int_dim_customer__crosswalk"])
    singleton = next(
        r for r in crosswalk if r["old_key"] == "orphan-7"
    )
    assert singleton["new_key"] == "legacy_cust_a:orphan-7"

    entity = _fetch_table(conn, executed["dim_customer"])
    assert any(r["customer_key"] == "legacy_cust_a:orphan-7" for r in entity)

    compat_a = conn.execute(
        f"SELECT COUNT(*) FROM {executed['stg_legacy_cust_a__compat']}"
    ).fetchone()[0]
    src_a = conn.execute(
        "SELECT COUNT(*) FROM ec_src_legacy_cust_a"
    ).fetchone()[0]
    assert compat_a == src_a == 2
    compat_b = conn.execute(
        f"SELECT COUNT(*) FROM {executed['stg_legacy_cust_b__compat']}"
    ).fetchone()[0]
    src_b = conn.execute(
        "SELECT COUNT(*) FROM ec_src_legacy_cust_b"
    ).fetchone()[0]
    assert compat_b == src_b == 1


def test_tie_sets_null_and_survivorship_review_status():
    from tests.test_entity_consolidation_engine import _base_request

    resp = RemodelEngine().remodel(_base_request())
    assert resp.status == "needs_survivorship_review"

    spec = _demo_spec()
    clusters = [
        {
            "new_key": "cust-tie",
            "rows": [
                {
                    "old_key": "1",
                    "old_table": "legacy_cust_a",
                    "timestamp": "2021-01-01T00:00:00",
                    "field_values": {
                        "customer_name": "Ann",
                        "city": "NY",
                        "updated_at": "2021-01-01",
                    },
                },
                {
                    "old_key": "2",
                    "old_table": "legacy_cust_b",
                    "timestamp": "2021-01-01T00:00:00",
                    "field_values": {
                        "customer_name": "Anne",
                        "city": "NY",
                        "updated_at": "2021-01-01",
                    },
                },
            ],
        }
    ]
    conn, executed = _run_spec(spec, clusters)
    row = next(
        r for r in _fetch_table(conn, executed["dim_customer"]) if r["customer_key"] == "cust-tie"
    )
    assert row["customer_name"] is None
    assert row["_survivorship_review"] is True


def _febrl_spec() -> EntityConsolidationSpec:
    return EntityConsolidationSpec(
        new_entity="dim_febrl_person",
        old_tables=["febrl_legacy_a", "febrl_legacy_b"],
        old_key_columns={
            "febrl_legacy_a": "record_id",
            "febrl_legacy_b": "record_id",
        },
        new_key_column="person_key",
        timestamp_column="source_ts",
        conflict_fields=["given_name", "surname", "postcode", "date_of_birth"],
    )


def _python_entity_values(clusters: list[dict], spec: EntityConsolidationSpec) -> dict:
    out: dict[str, dict[str, object | None]] = {}
    for cluster in clusters:
        new_key = str(cluster["new_key"])
        refs = [_source_record_from_dict(r) for r in cluster["rows"]]
        resolutions = classify_and_resolve(refs, spec.conflict_fields)
        out[new_key] = {
            field: (
                None
                if resolutions[field].resolved_values is None
                else resolutions[field].resolved_values.get(field)
            )
            for field in spec.conflict_fields
        }
    return out


def _sql_entity_values(
    conn,
    executed,
    spec: EntityConsolidationSpec,
    clusters: list[dict],
) -> dict:
    expected_keys = {str(c["new_key"]) for c in clusters}
    rows = _fetch_table(conn, executed[spec.new_entity])
    return {
        str(r[spec.new_key_column]): {
            field: r[field] for field in spec.conflict_fields
        }
        for r in rows
        if str(r[spec.new_key_column]) in expected_keys
    }


def _febrl_clusters() -> list[dict]:
    data = json.loads(FEBRL_FIXTURE.read_text())
    clusters = data["clusters"]
    for cluster in clusters:
        for row in cluster["rows"]:
            fv = row.setdefault("field_values", {})
            fv.setdefault("source_ts", row["timestamp"])
    return clusters


def _assert_python_sql_parity(clusters: list[dict]):
    spec = _febrl_spec()
    conn, executed = _run_spec(spec, clusters)
    py = _python_entity_values(clusters, spec)
    sql = _sql_entity_values(conn, executed, spec, clusters)
    assert set(py.keys()) == set(sql.keys())
    for new_key, fields in py.items():
        for field, expected in fields.items():
            got = sql[new_key][field]
            exp_norm = str(expected) if expected is not None else None
            got_norm = str(got) if got is not None else None
            assert exp_norm == got_norm, (
                f"{new_key}.{field}: python={expected!r} sql={got!r}"
            )


def test_febrl_differential_python_vs_sql_all_clusters():
    _assert_python_sql_parity(_febrl_clusters())


def test_febrl_differential_with_tied_timestamps_perturbation():
    clusters = copy.deepcopy(_febrl_clusters())
    tie_count = max(1, len(clusters) // 5)
    for cluster in clusters[:tie_count]:
        for row in cluster["rows"]:
            row["timestamp"] = "2020-06-15T12:00:00"
            row["field_values"]["source_ts"] = "2020-06-15 12:00:00"
    _assert_python_sql_parity(clusters)


def test_invalid_identifier_raises_value_error():
    spec = _demo_spec(new_entity="bad-name")
    with pytest.raises(ValueError, match="invalid SQL identifier"):
        validate_entity_consolidation_spec(spec)


def test_single_quote_in_cluster_value_round_trips_in_crosswalk_sql():
    spec = _demo_spec()
    clusters = [
        {
            "new_key": "cust-o'brien",
            "rows": [
                {
                    "old_key": "1",
                    "old_table": "legacy_cust_a",
                    "timestamp": "2020-01-01T00:00:00",
                    "field_values": {
                        "customer_name": "O''Brien",
                        "city": "NY",
                        "updated_at": "2020-01-01",
                    },
                }
            ],
        }
    ]
    sql = render_crosswalk_sql(spec, clusters)
    assert "cust-o''brien" in sql
    conn, executed = _run_spec(spec, clusters)
    crosswalk = _fetch_table(conn, executed["int_dim_customer__crosswalk"])
    assert crosswalk[0]["new_key"] == "cust-o'brien"
