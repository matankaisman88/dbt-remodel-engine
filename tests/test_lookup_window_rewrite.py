from pathlib import Path

import duckdb
import sqlglot
from sqlglot import exp
from remodel_engine.corpus import load_corpus_manifest
from remodel_engine.engine import RemodelEngine, _parity_context_from_request
from remodel_engine.star_shadowing import _jinja_to_parse_placeholders
from remodel_engine.refactor_rules import (
    LookupRewriteSpec,
    apply_lookup_window_rewrite,
    explain_gate,
)
from remodel_engine.sql_analysis import compile_dbt_sql

FIXTURES = Path(__file__).parent / "fixtures"
DAILY_ETL = FIXTURES / "daily_etl_main_corpus"


def _diagnosis_enriched_sql() -> str:
    return (DAILY_ETL / "models" / "raw_int_diagnosis_enriched.sql").read_text()


def _lookup_spec() -> LookupRewriteSpec:
    return LookupRewriteSpec(
        model_name="raw_int_diagnosis_enriched",
        lookup_alias="prov",
        order_by_column="provider_rank",
        partition_by_columns=["provider_id"],
        match_policy="single_match",
    )


def test_lookup_window_rewrite_targets_join_not_first_select():
    result = apply_lookup_window_rewrite(_diagnosis_enriched_sql(), _lookup_spec())
    assert result.window_functions_applied == 1
    assert not result.passthrough_reasons

    out = result.sql
    assert "lookup_prov" not in out.lower()
    assert "ROW_NUMBER()" in out
    assert "provider_rank" in out
    assert "rn_prov" in out

    diagnosis_cte = out.split("provider_lookup AS", maxsplit=1)[0]
    assert "ROW_NUMBER()" not in diagnosis_cte

    parse_sql, _ = _jinja_to_parse_placeholders(out)
    ast = sqlglot.parse_one(parse_sql, read="duckdb")
    joins = [
        j
        for j in ast.find_all(exp.Join)
        if j.this.alias and j.this.alias.lower() == "prov"
    ]
    assert len(joins) == 1
    join_sql = joins[0].this.sql(dialect="duckdb")
    assert "ROW_NUMBER()" in join_sql
    assert "provider_lookup" in join_sql or "provider_id" in join_sql


def test_daily_etl_corpus_lookup_rewrite_via_engine_explain():
    req = load_corpus_manifest(DAILY_ETL / "manifest.json")
    req.preferences.modernize_window_functions = True

    resp = RemodelEngine().remodel(req)
    enriched = next(
        m for m in resp.remodeled_models if m.model_name == "raw_int_diagnosis_enriched"
    )
    sql = enriched.sql

    assert "lookup_prov" not in sql.lower()
    assert "ROW_NUMBER()" in sql
    assert "PARTITION BY provider_id" in sql.upper() or "PARTITION BY provider_id" in sql
    assert "provider_rank" in sql

    parse_sql, _ = _jinja_to_parse_placeholders(sql)
    sqlglot.parse_one(parse_sql, read="duckdb")

    parity_ctx = _parity_context_from_request(req)
    assert parity_ctx is not None
    conn = duckdb.connect(":memory:")
    try:
        conn.execute(parity_ctx.seeds_sql)
        compiled = compile_dbt_sql(
            sql,
            parity_ctx.model_table_map,
            parity_ctx.source_table_map,
        )
        ok, msg = explain_gate(compiled, conn)
        assert ok, msg
    finally:
        conn.close()

    assert resp.refactoring_summary.window_functions_applied >= 1
