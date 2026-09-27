-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_vars"
  )
}}
-- Target: TGT_VARS
-- Informatica Load Order: 3
-- Source Instances: SRC_CUSTOMERS
WITH
    sq_sq_customers AS (
SELECT CUSTOMER_ID, REGION FROM {{ source('dbo', 'src_customers') }}
),

    int_exp_vars_prep AS (
    SELECT
        base.*,
        substr(RAW_DATE, 1, 10) AS PARSED_DATE
    FROM sq_sq_customers base

),

    int_exp_vars AS (
    SELECT
        base.*,
        PARSED_DATE AS FORMATTED_DATE
    FROM int_exp_vars_prep base

)

SELECT
    FORMATTED_DATE AS FORMATTED_DATE
FROM int_exp_vars

