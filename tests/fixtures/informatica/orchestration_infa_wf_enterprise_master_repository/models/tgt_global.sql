-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_global"
  )
}}
-- Target: TGT_GLOBAL
-- Informatica Load Order: 3
-- Source Instances: SRC_SALES
WITH
    sq_sq_sales AS (
SELECT CUSTOMER_ID, REGION, AMOUNT FROM {{ source('dbo', 'src_sales') }}
),

    int_agg_global AS (
    SELECT
        COUNT(1) AS ROW_COUNT,
        SUM(AMOUNT) AS TOTAL_AMOUNT
    FROM sq_sq_sales base

)

SELECT
    ROW_COUNT AS ROW_COUNT,
    TOTAL_AMOUNT AS TOTAL_AMOUNT
FROM int_agg_global

