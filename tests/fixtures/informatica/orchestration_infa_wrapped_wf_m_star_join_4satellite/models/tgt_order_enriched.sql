-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_order_enriched"
  )
}}
-- Target: TGT_ORDER_ENRICHED
-- Informatica Load Order: 1
-- Source Instances: SRC_CUSTOMER, SRC_ORDER_HEADER, SRC_PAYMENT, SRC_SHIPPING
WITH
    sq_sq_src_customer AS (
SELECT CUST_ID, CUST_NAME FROM {{ source('dbo', 'src_customer') }}
),

    sq_sq_order_header AS (
SELECT ORDER_ID, CUST_ID, SHIP_ID, PAY_ID FROM {{ source('dbo', 'src_order_header') }}
),

    int_jnr_cust AS (
    SELECT
        m.ORDER_ID,
        m.CUST_ID,
        m.SHIP_ID,
        m.PAY_ID,
        d.CUST_NAME
    FROM sq_sq_order_header m
    INNER JOIN sq_sq_src_customer d
        ON m.CUST_ID = d.CUST_ID

),

    sq_sq_src_payment AS (
SELECT PAY_ID, PAY_METHOD FROM {{ source('dbo', 'src_payment') }}
),

    sq_sq_src_shipping AS (
SELECT SHIP_ID, SHIP_METHOD FROM {{ source('dbo', 'src_shipping') }}
),

    int_jnr_ship AS (
    SELECT
        m.ORDER_ID,
        m.CUST_ID,
        m.SHIP_ID,
        m.PAY_ID,
        m.CUST_NAME,
        d.SHIP_METHOD
    FROM int_jnr_cust m
    INNER JOIN sq_sq_src_shipping d
        ON m.SHIP_ID = d.SHIP_ID

),

    int_jnr_pay AS (
    SELECT
        m.ORDER_ID,
        m.CUST_ID,
        m.SHIP_ID,
        m.PAY_ID,
        m.CUST_NAME,
        m.SHIP_METHOD,
        d.PAY_METHOD
    FROM int_jnr_ship m
    INNER JOIN sq_sq_src_payment d
        ON m.PAY_ID = d.PAY_ID

)

SELECT
    ORDER_ID AS ORDER_ID,
    CUST_NAME AS CUST_NAME,
    SHIP_METHOD AS SHIP_METHOD,
    PAY_METHOD AS PAY_METHOD
FROM int_jnr_pay

