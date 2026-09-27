-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
-- SCD Type 2 start column: START_DATE
-- SCD Type 2 end column: END_DATE
-- SCD Type 2 current row indicator: IS_CURRENT
{{
  config(
    materialized = 'snapshot',
    unique_key = 'CUST_ID_O',
    strategy = 'check',
    check_cols = ['CUST_NAME_O', 'REGION_O']
  )
}}
-- Target: TGT_DIM_CUSTOMER
-- Informatica Load Order: 1
-- Source Instances: SRC_CUSTOMER_DIM
WITH
    sq_sq_customer_dim AS (
SELECT CUST_ID, CUST_NAME, REGION, CHANGE_TYPE FROM {{ source('dbo', 'src_customer_dim') }}
),

    int_exp_scd_dates AS (
    SELECT
        base.*,
        CUST_ID AS CUST_ID_O,
        CUST_NAME AS CUST_NAME_O,
        REGION AS REGION_O,
        CURRENT_TIMESTAMP AS START_DATE,
        CAST(strptime('9999-12-31', '%Y-%m-%d') AS DATE) AS END_DATE,
        'Y' AS IS_CURRENT,
        CHANGE_TYPE AS CHANGE_TYPE_O
    FROM sq_sq_customer_dim base

),

    int_upd_scd AS (
    SELECT
        *,
        CASE CASE WHEN CHANGE_TYPE_O = 'UPDATE' THEN 1 ELSE 0 END WHEN 0 THEN 'I' WHEN 1 THEN 'U' WHEN 2 THEN 'D' WHEN 3 THEN 'R' ELSE 'R' END AS informatica_update_action
    FROM int_exp_scd_dates

)

SELECT
    CUST_ID_O AS CUST_ID_O,
    CUST_NAME_O AS CUST_NAME_O,
    REGION_O AS REGION_O,
    START_DATE AS START_DATE,
    END_DATE AS END_DATE,
    IS_CURRENT AS IS_CURRENT
FROM int_upd_scd
{% if is_incremental() %}
WHERE START_DATE > (SELECT coalesce(max(START_DATE), '1900-01-01') FROM {{ this }})
   OR CUST_ID_O NOT IN (SELECT CUST_ID_O FROM {{ this }})
{% endif %}

