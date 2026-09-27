"""Tests for CTAS star-shadowing harmonization."""

from remodel_engine.star_shadowing import fix_star_shadowing_for_ctas


def test_drops_join_column_shadowed_by_trailing_star() -> None:
    sql = """
SELECT
    base.DIAGNOSIS_PK AS DIAGNOSIS_PK_DIM,
    u0.DIAGNOSIS_PK AS DIAGNOSIS_PK,
    base.*
FROM {{ ref('int_exp_fields') }} base
LEFT JOIN {{ ref('int_lkp') }} u0 ON base.code = u0.code
"""
    fixed = fix_star_shadowing_for_ctas(sql)
    assert "u0.DIAGNOSIS_PK AS DIAGNOSIS_PK" not in fixed
    assert "base.*" in fixed
    assert "DIAGNOSIS_PK_DIM" in fixed


def test_keeps_rate_plan_lookup_and_expands_coalesce() -> None:
    bind_sql = """
SELECT
    base.RATE_PLAN_PK AS RATE_PLAN_PK_DIM,
    u4.RATE_PLAN_PK AS RATE_PLAN_PK,
    base.*
FROM {{ ref('int_exp_fields') }} base
LEFT JOIN {{ ref('lkp_lkp_ref_dim_rate_plan') }} u4 ON base.RATE_PLAN_CODE = u4.RATE_PLAN_CODE
"""
    fixed_bind = fix_star_shadowing_for_ctas(bind_sql)
    assert "u4.RATE_PLAN_PK AS RATE_PLAN_PK_LKP" in fixed_bind
    assert "u4.RATE_PLAN_PK AS RATE_PLAN_PK," not in fixed_bind

    exp_sql = """
SELECT
    base.*,
    COALESCE(RATE_PLAN_PK_DIM, RATE_PLAN_PK) AS RATE_PLAN_PK_OUT
FROM {{ ref('int_exp_bind') }} base
"""
    fixed_exp = fix_star_shadowing_for_ctas(exp_sql)
    assert "COALESCE(RATE_PLAN_PK_DIM, RATE_PLAN_PK_LKP, RATE_PLAN_PK)" in fixed_exp


def test_keeps_renamed_columns() -> None:
    sql = """
SELECT
    base.DIAGNOSIS_PK AS DIAGNOSIS_PK_DIM,
    u0.DIAGNOSIS_PK AS DIAGNOSIS_PK_LOOKUP,
    base.*
FROM {{ ref('int_exp_fields') }} base
LEFT JOIN {{ ref('int_lkp') }} u0 ON base.code = u0.code
"""
    fixed = fix_star_shadowing_for_ctas(sql)
    assert fixed.strip() == sql.strip()
