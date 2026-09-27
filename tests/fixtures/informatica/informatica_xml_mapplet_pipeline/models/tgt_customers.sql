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
-- Source Instances: SRC_CUSTOMERS
WITH
    sq_sq_customers AS (
SELECT CUSTOMER_NAME FROM {{ source('dbo', 'src_customers') }}
),

    map_mp_upper_inst_bind AS (
    SELECT
        CUSTOMER_NAME AS STR_IN,
        CUSTOMER_NAME AS STR
    FROM sq_sq_customers

),

    map_mp_upper_inst_exp_upper AS (
    SELECT
        *,
        upper(STR_IN) AS STR_OUT
    FROM map_mp_upper_inst_bind base

),

    int_mp_upper_inst AS (
    SELECT
        STR_OUT AS STR
    FROM map_mp_upper_inst_exp_upper

)

SELECT
    STR AS CUSTOMER_NAME
FROM int_mp_upper_inst

