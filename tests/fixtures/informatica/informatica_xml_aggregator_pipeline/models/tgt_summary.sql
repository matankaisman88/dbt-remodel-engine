-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_summary"
  )
}}
-- Target: TGT_SUMMARY
-- Informatica Load Order: 2
-- Source Instances: SRC_SALES
WITH
    sq_sq_sales AS (
SELECT CUSTOMER_ID, REGION, AMOUNT FROM {{ source('dbo', 'src_sales') }}
),

    int_agg_summary AS (
    SELECT
        REGION,
        SUM(AMOUNT) AS TOTAL_AMOUNT,
        COUNT(1) AS ROW_COUNT,
        MAX(AMOUNT) AS MAX_AMOUNT
    FROM sq_sq_sales base
    GROUP BY REGION

)

SELECT
    REGION AS REGION,
    TOTAL_AMOUNT AS TOTAL_AMOUNT,
    ROW_COUNT AS ROW_COUNT,
    MAX_AMOUNT AS MAX_AMOUNT
FROM int_agg_summary

