"""Tests for CTAS star-shadowing harmonization."""

from remodel_engine.schema import ShadowedLookupRenameSpec
from remodel_engine.star_shadowing import fix_star_shadowing_for_ctas

RATE_PLAN_SHADOW_SPEC = ShadowedLookupRenameSpec(
    model_name="bind_model",
    dim_column="RATE_PLAN_PK_DIM",
    base_column="RATE_PLAN_PK",
    renamed_column="RATE_PLAN_PK_LKP",
    lookup_ref_pattern="ref_dim_rate_plan",
)


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
    fixed_bind = fix_star_shadowing_for_ctas(
        bind_sql,
        model_name="bind_model",
        shadowed_lookup_renames=[RATE_PLAN_SHADOW_SPEC],
    )
    assert "u4.RATE_PLAN_PK AS RATE_PLAN_PK_LKP" in fixed_bind
    assert "u4.RATE_PLAN_PK AS RATE_PLAN_PK," not in fixed_bind

    exp_sql = """
SELECT
    base.*,
    COALESCE(RATE_PLAN_PK_DIM, RATE_PLAN_PK) AS RATE_PLAN_PK_OUT
FROM {{ ref('int_exp_bind') }} base
"""
    fixed_exp = fix_star_shadowing_for_ctas(
        exp_sql,
        model_name="bind_model",
        shadowed_lookup_renames=[RATE_PLAN_SHADOW_SPEC],
        renamed_column_present=True,
    )
    assert "COALESCE(RATE_PLAN_PK_DIM, RATE_PLAN_PK_LKP, RATE_PLAN_PK)" in fixed_exp


def test_decomposed_rate_plan_ref_keeps_lookup_and_expands_qualified_coalesce() -> None:
    bind_sql = """
SELECT
    base.RATE_PLAN_PK AS RATE_PLAN_PK_DIM,
    u4.RATE_PLAN_PK AS RATE_PLAN_PK,
    base.*
FROM {{ ref('int_exp_fields') }} base
LEFT JOIN {{ ref('int_lkp_ref_dim_rate_plan') }} u4 ON base.RATE_PLAN_CODE = u4.RATE_PLAN_CODE
"""
    fixed_bind = fix_star_shadowing_for_ctas(
        bind_sql,
        model_name="bind_model",
        shadowed_lookup_renames=[RATE_PLAN_SHADOW_SPEC],
    )
    assert "u4.RATE_PLAN_PK AS RATE_PLAN_PK_LKP" in fixed_bind

    exp_sql = """
SELECT
    COALESCE(base.RATE_PLAN_PK_DIM, base.RATE_PLAN_PK) AS RATE_PLAN_PK_OUT
FROM {{ ref('int_exp_prep') }} base
"""
    fixed_exp = fix_star_shadowing_for_ctas(
        exp_sql,
        model_name="bind_model",
        shadowed_lookup_renames=[RATE_PLAN_SHADOW_SPEC],
        renamed_column_present=True,
    )
    assert (
        "COALESCE(base.RATE_PLAN_PK_DIM, base.RATE_PLAN_PK_LKP, base.RATE_PLAN_PK)"
        in fixed_exp
    )


def test_manifest_shadow_spec_generalizes_to_other_column_names() -> None:
    account_spec = ShadowedLookupRenameSpec(
        model_name="stg_account_bind",
        dim_column="ACCOUNT_SK_DIM",
        base_column="ACCOUNT_SK",
        renamed_column="ACCOUNT_SK_LKP",
        lookup_ref_pattern="ref_dim_account",
    )
    bind_sql = """
SELECT
    base.ACCOUNT_SK AS ACCOUNT_SK_DIM,
    u2.ACCOUNT_SK AS ACCOUNT_SK,
    base.*
FROM {{ ref('int_exp_fields') }} base
LEFT JOIN {{ ref('lkp_ref_dim_account') }} u2 ON base.ACCOUNT_CODE = u2.ACCOUNT_CODE
"""
    fixed_bind = fix_star_shadowing_for_ctas(
        bind_sql,
        model_name="stg_account_bind",
        shadowed_lookup_renames=[account_spec],
    )
    assert "u2.ACCOUNT_SK AS ACCOUNT_SK_LKP" in fixed_bind

    exp_sql = """
SELECT COALESCE(ACCOUNT_SK_DIM, ACCOUNT_SK) AS ACCOUNT_SK_OUT
FROM {{ ref('int_exp_bind') }}
"""
    fixed_exp = fix_star_shadowing_for_ctas(
        exp_sql,
        model_name="stg_account_bind",
        shadowed_lookup_renames=[account_spec],
        renamed_column_present=True,
    )
    assert "COALESCE(ACCOUNT_SK_DIM, ACCOUNT_SK_LKP, ACCOUNT_SK)" in fixed_exp


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
