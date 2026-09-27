from remodel_engine.parity_gate import ParityContext, run_parity_gate


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
