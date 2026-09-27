from remodel_engine.layer_synthesizer import Layer, classify_model
from remodel_engine.parity_gate import (
    ParityContext,
    grain_risk_requires_manual_review,
    run_parity_gate,
)


def test_parity_gate_pass_identical_sql():
    ctx = ParityContext(
        seeds_sql="CREATE TABLE t AS SELECT 1 AS id, 'a' AS name",
        model_table_map={},
        source_table_map={},
    )
    sql = "SELECT id, name FROM t"
    result = run_parity_gate(
        model_name="m",
        raw_sql=sql,
        remodeled_sql=sql,
        context=ctx,
    )
    assert result.status == "pass"


def test_parity_gate_grain_risk_skips_execution():
    ctx = ParityContext(
        seeds_sql="CREATE TABLE t AS SELECT 1 AS id",
        model_table_map={},
        source_table_map={},
    )
    sql = "SELECT id, COUNT(*) FROM t GROUP BY id"
    result = run_parity_gate(
        model_name="m",
        raw_sql=sql,
        remodeled_sql=sql,
        context=ctx,
        gate_grain_risk=True,
    )
    assert result.status == "needs_manual_review"
    assert result.trace_rule


def test_parity_gate_fail_on_row_diff():
    ctx = ParityContext(
        seeds_sql="CREATE TABLE t AS SELECT 1 AS id",
        model_table_map={},
        source_table_map={},
    )
    result = run_parity_gate(
        model_name="m",
        raw_sql="SELECT id FROM t",
        remodeled_sql="SELECT id + 1 AS id FROM t",
        context=ctx,
    )
    assert result.status == "fail"


def test_benign_rule2_expression_passes_grain_gate_and_parity():
    sql = """
    SELECT
      customer_id,
      UPPER(customer_name) AS customer_name,
      CASE WHEN credit_group = 'A' THEN 'Y' ELSE 'N' END AS preferred_flag
    FROM {{ ref('raw_stg_customers') }}
    """
    classification = classify_model("raw_int_exp", sql)
    assert classification.layer == Layer.INTERMEDIATE
    assert not classification.flagged
    assert "matched rule #2" in classification.classification_reason

    risky, reason = grain_risk_requires_manual_review(sql)
    assert not risky
    assert reason is None

    ctx = ParityContext(
        seeds_sql=(
            "CREATE TABLE raw_stg_customers AS "
            "SELECT 1 AS customer_id, 'x' AS customer_name, 'A' AS credit_group"
        ),
        model_table_map={"raw_stg_customers": "raw_stg_customers"},
        source_table_map={},
    )
    result = run_parity_gate(
        model_name="raw_int_exp",
        raw_sql=sql,
        remodeled_sql=sql,
        context=ctx,
        gate_grain_risk=True,
    )
    assert result.status == "pass"
