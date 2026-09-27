-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_product_names_clean"
  )
}}
-- Target: TGT_PRODUCT_NAMES_CLEAN
-- Informatica Load Order: 1
-- Source Instances: SRC_PRODUCT_NAMES
WITH
    sq_sq_product_names AS (
SELECT PRODUCT_NAME FROM {{ source('dbo', 'src_product_names') }}
),

    map_mp_normalize_product_bind AS (
    SELECT
        PRODUCT_NAME AS STR_IN,
        PRODUCT_NAME AS STR
    FROM sq_sq_product_names

),

    map_mp_normalize_product_exp_normalize AS (
    SELECT
        *,
        upper(ltrim(rtrim(STR_IN))) AS STR_OUT
    FROM map_mp_normalize_product_bind base

),

    int_mp_normalize_product AS (
    SELECT
        STR_OUT AS STR
    FROM map_mp_normalize_product_exp_normalize

)

SELECT
    STR AS PRODUCT_NAME
FROM int_mp_normalize_product

