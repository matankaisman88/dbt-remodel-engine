-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_sales_rollup"
  )
}}
-- Target: TGT_SALES_ROLLUP
-- Informatica Load Order: 1
-- Source Instances: SRC_SALES_DETAIL
WITH
    sq_sq_sales_detail AS (
SELECT YEAR, QUARTER, REGION, PRODUCT_LINE, AMT FROM {{ source('dbo', 'src_sales_detail') }}
),

    int_agg_multi_group AS (
    SELECT
        YEAR,
        QUARTER,
        REGION,
        PRODUCT_LINE,
        SUM(AMT) AS TOTAL_AMT,
        AVG(AMT) AS AVG_AMT,
        MAX(AMT) AS MAX_AMT
    FROM sq_sq_sales_detail base
    GROUP BY YEAR, QUARTER, REGION, PRODUCT_LINE

)

SELECT
    YEAR AS YEAR,
    QUARTER AS QUARTER,
    REGION AS REGION,
    PRODUCT_LINE AS PRODUCT_LINE,
    TOTAL_AMT AS TOTAL_AMT,
    AVG_AMT AS AVG_AMT,
    MAX_AMT AS MAX_AMT
FROM int_agg_multi_group

