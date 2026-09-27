-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'incremental',
    incremental_strategy = 'append',
    unique_key = 'ORDER_ID',
    schema = "dbo",
    alias = "tgt_orders"
  )
}}
-- Target: TGT_ORDERS
-- Informatica Load Order: 1
-- Source Instances: SRC_ORDERS
WITH
    sq_sq_orders AS (
SELECT ORDER_ID, CUSTOMER_NAME FROM {{ source('dbo', 'src_orders') }}
),

    int_exp_orders AS (
    SELECT
        base.ORDER_ID,
        upper(CUSTOMER_NAME) AS CUSTOMER_NAME
    FROM sq_sq_orders base

),

    int_upd_orders AS (
    SELECT
        *,
        'I' AS informatica_update_action
    FROM int_exp_orders

)

SELECT
    ORDER_ID AS ORDER_ID,
    CAST(NULL AS INTEGER) /* unmapped in source mapping */ AS CUSTOMER_ID,
    CAST(NULL AS VARCHAR) /* unmapped in source mapping */ AS CREATED_DATE
FROM int_upd_orders
{% if is_incremental() %}
WHERE CREATED_DATE > (SELECT coalesce(max(CREATED_DATE), '1900-01-01') FROM {{ this }})
   OR ORDER_ID NOT IN (SELECT ORDER_ID FROM {{ this }})
{% endif %}

