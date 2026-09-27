"""End-to-end RemodelEngine coverage for physical_decompose (committed corpus)."""

from __future__ import annotations

from pathlib import Path

import duckdb
import sqlglot
from remodel_engine.corpus import load_corpus_manifest
from remodel_engine.engine import RemodelEngine, _parity_context_from_request
from remodel_engine.physical_decomposer import PhysicalModel, topological_model_order
from remodel_engine.refactor_rules import explain_gate
from remodel_engine.sql_analysis import compile_dbt_sql, extract_refs
from remodel_engine.star_shadowing import _jinja_to_parse_placeholders

FIXTURE = (
    Path(__file__).parent / "fixtures" / "physical_decompose_wwi_corpus" / "manifest.json"
)


def _assert_sqlglot_parseable(sql: str) -> None:
    parse_sql, _ = _jinja_to_parse_placeholders(sql)
    sqlglot.parse_one(parse_sql, read="duckdb")


def test_physical_decompose_wwi_corpus_end_to_end() -> None:
    req = load_corpus_manifest(FIXTURE)
    assert req.preferences.physical_decompose is True
    assert len(req.raw_dbt_models) == 3

    resp = RemodelEngine().remodel(req)
    assert resp.refactoring_summary.shared_models_extracted >= 1
    assert len(resp.remodeled_models) > len(req.raw_dbt_models)

    emitted_names = {m.model_name for m in resp.remodeled_models}

    for model in resp.remodeled_models:
        _assert_sqlglot_parseable(model.sql)
        for ref_name in extract_refs(model.sql):
            assert ref_name in emitted_names, (
                f"{model.model_name}: ref('{ref_name}') not in emitted models"
            )

    parity_ctx = _parity_context_from_request(req)
    assert parity_ctx is not None
    conn = duckdb.connect(":memory:")
    try:
        conn.execute(parity_ctx.seeds_sql)
        runtime_map = dict(parity_ctx.model_table_map)
        by_name = {m.model_name: m for m in resp.remodeled_models}
        physical = [
            PhysicalModel(
                model_name=m.model_name,
                relative_path=m.relative_path or f"models/{m.model_name}.sql",
                sql=m.sql,
                layer=m.layer,
            )
            for m in resp.remodeled_models
        ]
        for name in topological_model_order(physical):
            model = by_name[name]
            compiled = compile_dbt_sql(
                model.sql,
                runtime_map,
                parity_ctx.source_table_map,
            )
            ok, msg = explain_gate(compiled, conn)
            assert ok, f"EXPLAIN failed for {name}: {msg}"
            table = f"remodel_{name}"
            conn.execute(f"CREATE OR REPLACE TABLE {table} AS {compiled}")
            runtime_map[name] = table
    finally:
        conn.close()

    checked = [
        m
        for m in resp.remodeled_models
        if m.parity_check.status != "skipped"
    ]
    assert checked, "expected parity checks on decomposed intermediates and marts"
    assert all(m.parity_check.status == "pass" for m in checked)
    assert resp.status == "success"
