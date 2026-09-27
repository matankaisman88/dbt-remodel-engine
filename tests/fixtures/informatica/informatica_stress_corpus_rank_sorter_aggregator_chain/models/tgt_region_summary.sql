-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_region_summary"
  )
}}
-- Target: TGT_REGION_SUMMARY
-- Informatica Load Order: 1
-- Source Instances: SRC_SALES
WITH
    sq_sq_sales AS (
SELECT SALESPERSON, REGION, AMT FROM {{ source('dbo', 'src_sales') }}
),

    int_rnk_top_sales AS (
    SELECT *
    FROM (
        SELECT
        base.SALESPERSON,
        base.REGION,
        base.AMT,
        ROW_NUMBER() OVER (PARTITION BY base.REGION ORDER BY 1 DESC) AS RANKINDEX
        FROM sq_sq_sales base
    ) ranked
    WHERE RANKINDEX <= 10

),

    int_srt_by_amt AS (
    SELECT *
    FROM int_rnk_top_sales

),

    int_agg_region_total AS (
    SELECT
        REGION,
        SUM(AMT) AS TOTAL_AMT,
        COUNT(SALESPERSON) AS SALES_COUNT
    FROM int_srt_by_amt base
    GROUP BY REGION

)

SELECT
    REGION AS REGION,
    TOTAL_AMT AS TOTAL_AMT,
    SALES_COUNT AS SALES_COUNT
FROM int_agg_region_total

