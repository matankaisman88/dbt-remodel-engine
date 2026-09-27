-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_orders"
  )
}}
-- Target: TGT_ORDERS
-- Informatica Load Order: 2
-- Source Instances: FCT_ORDERS
WITH
    sq_sq_orders AS (
SELECT ORDER_ID, CUSTOMER_ID FROM {{ source('dw_core', 'fct_orders') }}
),

    int_exp_orders AS (
    SELECT
        base.*,
        CURRENT_TIMESTAMP AS CREATED_DATE
    FROM sq_sq_orders base

)

SELECT
    ORDER_ID AS ORDER_ID,
    CUSTOMER_ID AS CUSTOMER_ID,
    CREATED_DATE AS CREATED_DATE
FROM int_exp_orders

