from remodel_engine.refactor_rules import (
    LookupRewriteSpec,
    apply_lookup_window_rewrite,
    assess_rule2,
    collapse_eligible_ctes,
)


def test_collapses_filter_only_cte():
    sql = """
WITH base AS (
  SELECT id, name FROM t
),
filtered AS (
  SELECT id, name FROM base WHERE id IS NOT NULL
)
SELECT * FROM filtered
"""
    result = collapse_eligible_ctes(sql, enabled=True)
    assert result.ctes_collapsed >= 1
    assert result.merge_audits


def test_blocks_multi_consumer_window_cte_merge():
    sql = """
WITH ranked AS (
  SELECT id, ROW_NUMBER() OVER (PARTITION BY id ORDER BY id) AS rn FROM t
),
a AS (SELECT id, rn FROM ranked),
b AS (SELECT id, COUNT(*) FROM ranked GROUP BY id)
SELECT * FROM a JOIN b USING (id)
"""
    result = collapse_eligible_ctes(sql, enabled=True)
    assert any("forbidden merge" in m for m in result.blocked_merges)


def test_assess_rule2_ref_projection_is_intermediate():
    sql = "SELECT id, UPPER(name) AS name FROM {{ ref('stg_x') }}"
    result = assess_rule2(sql)
    assert result.layer_intermediate
    assert not result.needs_manual_review


def test_assess_rule2_group_by_needs_manual_review():
    sql = """
    SELECT customer_id, COUNT(*) AS n
    FROM {{ ref('stg_orders') }}
    GROUP BY customer_id
    """
    result = assess_rule2(sql)
    assert result.needs_manual_review
    assert "GROUP BY" in result.classification_reason


def test_lookup_rewrite_fail_closed_on_ambiguous_policy():
    spec = LookupRewriteSpec(
        model_name="m",
        lookup_alias="prov",
        order_by_column="rank",
        match_policy="take_any",
    )
    result = apply_lookup_window_rewrite("SELECT 1", spec, enabled=True)
    assert result.passthrough_reasons
    assert result.window_functions_applied == 0


def test_lookup_rewrite_parse_failure_is_passthrough():
    spec = LookupRewriteSpec(
        model_name="m",
        lookup_alias="prov",
        order_by_column="rank",
        partition_by_columns=["provider_id"],
    )
    result = apply_lookup_window_rewrite("SELECT {{{{", spec, enabled=True)
    assert result.sql == "SELECT {{{{"
    assert any("parse failed" in r for r in result.passthrough_reasons)
