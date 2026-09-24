from remodel_engine.layer_synthesizer import Layer, LegacyTargetMeta, classify_model


def test_staging_source_only_rename_cast():
    sql = """
    SELECT
      id AS customer_id,
      CAST(name AS VARCHAR) AS customer_name
    FROM {{ source('wwi', 'customers') }}
    """
    result = classify_model("raw_stg_customers", sql)
    assert result.layer == Layer.STAGING
    assert not result.flagged


def test_staging_rejects_join_fail_closed():
    sql = """
    SELECT a.id, b.id
    FROM {{ source('wwi', 'customers') }} a
    JOIN {{ source('wwi', 'invoice_lines') }} b ON a.id = b.customer_id
    """
    result = classify_model("raw_bad_stg", sql)
    assert result.layer == Layer.NEEDS_MANUAL_REVIEW
    assert result.flagged


def test_intermediate_before_marts_on_legacy_target_with_join():
    sql = """
    SELECT d.id, c.name
    FROM {{ ref('raw_stg_customers') }} c
    JOIN {{ source('wwi', 'invoice_lines') }} d ON c.customer_id = d.customer_id
    """
    legacy = {
        "raw_int_sales": LegacyTargetMeta(
            target_name="DIM_X", last_transformation_type="update_strategy_scd"
        )
    }
    result = classify_model("raw_int_sales", sql, legacy_targets=legacy)
    assert result.layer == Layer.INTERMEDIATE


def test_marts_legacy_target_when_not_staging_eligible():
    sql = """
    SELECT
      customer_id,
      customer_name,
      CASE WHEN credit_group = 'A' THEN 'Y' ELSE 'N' END AS preferred_flag
    FROM {{ source('wwi', 'customers') }}
    """
    legacy = {
        "raw_tgt_dim": LegacyTargetMeta(
            target_name="DIM_CUSTOMER", last_transformation_type="update_strategy_scd"
        )
    }
    result = classify_model("raw_tgt_dim", sql, legacy_targets=legacy)
    assert result.layer == Layer.MARTS
    assert result.suggested_name == "dim_tgt_dim"


def test_fail_closed_ref_only_no_transform_signals():
    sql = "SELECT customer_id FROM {{ ref('raw_stg_customers') }}"
    result = classify_model("raw_passthrough", sql)
    assert result.layer == Layer.NEEDS_MANUAL_REVIEW
    assert result.flagged


def test_fail_closed_unknown_mart_transformation_type():
    sql = """
    SELECT customer_id,
      CASE WHEN credit_group = 'A' THEN 1 ELSE 0 END AS preferred_flag
    FROM {{ source('wwi', 'customers') }}
    """
    legacy = {
        "raw_x": LegacyTargetMeta(
            target_name="TGT", last_transformation_type="unknown_transformation"
        )
    }
    result = classify_model("raw_x", sql, legacy_targets=legacy)
    assert result.layer == Layer.NEEDS_MANUAL_REVIEW
