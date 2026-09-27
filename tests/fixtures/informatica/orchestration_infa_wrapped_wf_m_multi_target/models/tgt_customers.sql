-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_customers"
  )
}}
-- Target: TGT_CUSTOMERS
-- Informatica Load Order: 1
-- Source Instances: DIM_CUSTOMERS
WITH
    sq_sq_customers AS (
SELECT CUSTOMER_ID, CUSTOMER_NAME FROM {{ source('dw_core', 'dim_customers') }} WHERE IS_DELETED = 0
),

    int_exp_customers AS (
    SELECT
        base.CUSTOMER_ID,
        upper(CUSTOMER_NAME) AS CUSTOMER_NAME,
        CURRENT_TIMESTAMP AS CREATED_DATE
    FROM sq_sq_customers base

)

SELECT
    CUSTOMER_ID AS CUSTOMER_ID,
    CUSTOMER_NAME AS CUSTOMER_NAME,
    CREATED_DATE AS CREATED_DATE
FROM int_exp_customers

