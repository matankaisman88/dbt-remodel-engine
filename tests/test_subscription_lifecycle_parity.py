"""Parity regression for subscription lifecycle RATE_PLAN_PK / COALESCE / star shadowing."""

from __future__ import annotations

from pathlib import Path

import duckdb

from remodel_engine.corpus import load_corpus_manifest
from remodel_engine.engine import RemodelEngine
from remodel_engine.star_shadowing import fix_star_shadowing_for_ctas

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "_tmp_compile"
MANIFEST = BUNDLE / "manifest.json"


def test_subscription_lifecycle_rate_plan_pk_coalesce_after_ctas() -> None:
    """Decomposed int_exp_bind CTAS must keep lookup RATE_PLAN_PK for COALESCE parity."""
    conn = duckdb.connect()
    conn.execute(
        """
        CREATE TABLE int_exp_fields AS
        SELECT
            CAST(NULL AS DECIMAL(18, 3)) AS rate_plan_pk,
            CAST('-1' AS VARCHAR) AS rate_plan_code
        """
    )
    conn.execute(
        """
        CREATE TABLE lkp_lkp_ref_dim_rate_plan AS
        SELECT
            CAST('12.340' AS DECIMAL(18, 3)) AS rate_plan_pk,
            CAST('-1' AS VARCHAR) AS rate_plan_code
        """
    )
    bind_sql_raw = """
SELECT
    base.RATE_PLAN_PK AS RATE_PLAN_PK_DIM,
    u4.RATE_PLAN_PK AS RATE_PLAN_PK,
    base.*
FROM int_exp_fields base
LEFT JOIN lkp_lkp_ref_dim_rate_plan u4 ON base.RATE_PLAN_CODE = u4.RATE_PLAN_CODE
"""
    bind_sql = fix_star_shadowing_for_ctas(bind_sql_raw)
    raw_out = conn.execute(
        f"""
        WITH int_exp_bind AS ({bind_sql_raw}),
        int_exp AS (
            SELECT
                base.*,
                COALESCE(RATE_PLAN_PK_DIM, RATE_PLAN_PK) AS RATE_PLAN_PK_OUT
            FROM int_exp_bind base
        )
        SELECT RATE_PLAN_PK_OUT FROM int_exp
        """
    ).fetchone()[0]

    conn.execute(f"CREATE TABLE int_exp_bind AS {bind_sql}")
    rem_sql = fix_star_shadowing_for_ctas(
        """
SELECT COALESCE(RATE_PLAN_PK_DIM, RATE_PLAN_PK) AS RATE_PLAN_PK_OUT
FROM int_exp_bind
""",
        source_has_rate_plan_lkp=True,
    )
    rem_out = conn.execute(rem_sql).fetchone()[0]

    assert raw_out is not None
    assert rem_out == raw_out


pytestmark_bundle = __import__("pytest").mark.skipif(
    not MANIFEST.is_file()
    or not any(
        "subscription_lifecycle" in p.name
        for p in (BUNDLE / "models").glob("*.sql")
    ),
    reason="_tmp_compile subscription_lifecycle bundle required",
)


@pytestmark_bundle
def test_fct_shortcut_to_stg_subscription_lifecycle_marts_parity() -> None:
    req = load_corpus_manifest(MANIFEST)
    assert req.preferences.physical_decompose is True
    resp = RemodelEngine().remodel(req)
    marts = [
        m
        for m in resp.remodeled_models
        if m.parity_check.status != "skipped"
        and "subscription_lifecycle" in m.model_name
    ]
    assert marts, "expected at least one subscription_lifecycle mart with parity enabled"
    assert all(m.parity_check.status == "pass" for m in marts)
