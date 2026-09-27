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

)

SELECT
    ORDER_ID AS ORDER_ID,
    CAST(NULL AS INTEGER) /* unmapped in source mapping */ AS CUSTOMER_ID,
    CAST(NULL AS VARCHAR) /* unmapped in source mapping */ AS CREATED_DATE
FROM int_exp_orders

