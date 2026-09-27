-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_supplier_names_clean"
  )
}}
-- Target: TGT_SUPPLIER_NAMES_CLEAN
-- Informatica Load Order: 2
-- Source Instances: SRC_SUPPLIER_NAMES
WITH
    sq_sq_supplier_names AS (
SELECT SUPPLIER_NAME FROM {{ source('dbo', 'src_supplier_names') }}
),

    map_mp_normalize_supplier_bind AS (
    SELECT
        SUPPLIER_NAME AS STR_IN,
        SUPPLIER_NAME AS STR
    FROM sq_sq_supplier_names

),

    map_mp_normalize_supplier_exp_normalize AS (
    SELECT
        *,
        upper(ltrim(rtrim(STR_IN))) AS STR_OUT
    FROM map_mp_normalize_supplier_bind base

),

    int_mp_normalize_supplier AS (
    SELECT
        STR_OUT AS STR
    FROM map_mp_normalize_supplier_exp_normalize

)

SELECT
    STR AS SUPPLIER_NAME
FROM int_mp_normalize_supplier

