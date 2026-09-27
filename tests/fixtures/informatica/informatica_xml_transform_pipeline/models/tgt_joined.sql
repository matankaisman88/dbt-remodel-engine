-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_joined"
  )
}}
-- Target: TGT_JOINED
-- Informatica Load Order: 1
-- Source Instances: SRC_CUSTOMERS, SRC_ORDERS
WITH
    sq_sq_customers AS (
SELECT CUSTOMER_ID, REGION FROM {{ source('dbo', 'src_customers') }}
),

    sq_sq_orders AS (
SELECT ORDER_ID, CUSTOMER_ID FROM {{ source('dbo', 'src_orders') }}
),

    int_jnr_orders AS (
    SELECT
        d.ORDER_ID,
        d.CUSTOMER_ID,
        m.REGION
    FROM sq_sq_customers m
    INNER JOIN sq_sq_orders d
        ON m.CUSTOMER_ID = d.CUSTOMER_ID

),

    int_rtr_region AS (
    SELECT
        base.ORDER_ID,
        base.REGION
    FROM int_jnr_orders base
    WHERE REGION = 'EMEA'

)

SELECT
    ORDER_ID AS ORDER_ID,
    REGION AS REGION
FROM int_rtr_region

