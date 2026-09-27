-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_distinct"
  )
}}
-- Target: TGT_DISTINCT
-- Informatica Load Order: 1
-- Source Instances: SRC_SALES
WITH
    sq_sq_sales AS (
SELECT CUSTOMER_ID, REGION, AMOUNT FROM {{ source('dbo', 'src_sales') }}
),

    int_agg_distinct AS (
    SELECT
        CUSTOMER_ID
    FROM sq_sq_sales base
    GROUP BY CUSTOMER_ID

)

SELECT
    CUSTOMER_ID AS CUSTOMER_ID
FROM int_agg_distinct

