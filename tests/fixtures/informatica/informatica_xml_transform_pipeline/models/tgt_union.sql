-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_union"
  )
}}
-- Target: TGT_UNION
-- Informatica Load Order: 2
-- Source Instances: SRC_CUSTOMERS, SRC_ORDERS
WITH
    sq_sq_customers AS (
SELECT CUSTOMER_ID, REGION FROM {{ source('dbo', 'src_customers') }}
),

    sq_sq_orders AS (
SELECT ORDER_ID, CUSTOMER_ID FROM {{ source('dbo', 'src_orders') }}
),

    int_un_orders AS (
    SELECT
        ORDER_ID,
        NULL AS REGION
    FROM sq_sq_orders
    UNION ALL
    SELECT
        NULL AS ORDER_ID,
        REGION
    FROM sq_sq_customers

)

SELECT
    ORDER_ID AS ORDER_ID,
    REGION AS REGION
FROM int_un_orders

