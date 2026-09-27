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
