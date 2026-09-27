-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{# manual_review_required: set unique_key #}
{{
  config(
    materialized = 'incremental',
    incremental_strategy = 'append',
    schema = "dbo",
    alias = "tgt_customer_scd"
  )
}}
-- Target: TGT_CUSTOMER_SCD
-- Informatica Load Order: 1
-- Source Instances: SRC_CUSTOMER_CHANGES
WITH
    sq_sq_customer_changes AS (
SELECT CUST_ID, CUST_NAME, CHANGE_TYPE FROM {{ source('dbo', 'src_customer_changes') }}
),

    int_exp_build_row AS (
    SELECT
        base.*,
        ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS SURROGATE_KEY,
        CUST_ID AS CUST_ID_O,
        CUST_NAME AS CUST_NAME_O,
        CHANGE_TYPE AS CHANGE_TYPE_O
    FROM sq_sq_customer_changes base

),

    int_upd_apply_change AS (
    SELECT
        *,
        CASE CASE WHEN CHANGE_TYPE_O = 'DELETE' THEN 2 WHEN CHANGE_TYPE_O = 'UPDATE' THEN 1 ELSE 0 END WHEN 0 THEN 'I' WHEN 1 THEN 'U' WHEN 2 THEN 'D' WHEN 3 THEN 'R' ELSE 'R' END AS informatica_update_action
    FROM int_exp_build_row

)

SELECT
    SURROGATE_KEY AS SURROGATE_KEY,
    CUST_ID_O AS CUST_ID_O,
    CUST_NAME_O AS CUST_NAME_O
FROM int_upd_apply_change
{% if is_incremental() %}
WHERE informatica_update_action != 'R'
{% endif %}

