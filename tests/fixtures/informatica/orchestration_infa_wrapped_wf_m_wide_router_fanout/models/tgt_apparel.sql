-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_apparel"
  )
}}
-- Target: TGT_APPAREL
-- Informatica Load Order: 2
-- Source Instances: SRC_ORDERS
WITH
    sq_sq_orders AS (
SELECT ORDER_ID, CATEGORY, AMT FROM {{ source('dbo', 'src_orders') }}
),

    int_rtr_category AS (
    SELECT
        *
    FROM sq_sq_orders base

)

SELECT
    ORDER_ID AS ORDER_ID,
    CATEGORY AS CATEGORY,
    AMT AS AMT
FROM int_rtr_category

