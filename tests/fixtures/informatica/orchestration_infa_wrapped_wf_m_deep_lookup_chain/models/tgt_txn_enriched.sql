-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_txn_enriched"
  )
}}
-- Target: TGT_TXN_ENRICHED
-- Informatica Load Order: 1
-- Source Instances: SRC_TXN
WITH
    sq_sq_txn AS (
SELECT TXN_ID, CUST_ID, AMT FROM {{ source('dbo', 'src_txn') }}
),

    lkp_lkp_cust AS (
    SELECT
        src.*,
        lkp.CUST_NAME AS CUST_NAME,
        lkp.REGION_ID AS REGION_ID
    FROM sq_sq_txn src
    LEFT JOIN {{ source('dbo', 'ref_customer') }} lkp
        ON TRY_CAST(lkp.CUST_ID AS VARCHAR) = TRY_CAST(src.CUST_ID AS VARCHAR)

),

    lkp_lkp_region AS (
    SELECT
        src.*,
        lkp.REGION_NAME AS REGION_NAME,
        lkp.COUNTRY_ID AS COUNTRY_ID
    FROM lkp_lkp_cust src
    LEFT JOIN {{ source('dbo', 'ref_region') }} lkp
        ON TRY_CAST(lkp.REGION_ID AS VARCHAR) = TRY_CAST(src.REGION_ID AS VARCHAR)

),

    lkp_lkp_country AS (
    SELECT
        src.*,
        lkp.COUNTRY_NAME AS COUNTRY_NAME,
        lkp.CURRENCY_ID AS CURRENCY_ID
    FROM lkp_lkp_region src
    LEFT JOIN {{ source('dbo', 'ref_country') }} lkp
        ON TRY_CAST(lkp.COUNTRY_ID AS VARCHAR) = TRY_CAST(src.COUNTRY_ID AS VARCHAR)

),

    lkp_lkp_currency AS (
    SELECT
        src.*,
        lkp.CURRENCY_CODE AS CURRENCY_CODE,
        lkp.FX_RATE_ID AS FX_RATE_ID
    FROM lkp_lkp_country src
    LEFT JOIN {{ source('dbo', 'ref_currency') }} lkp
        ON TRY_CAST(lkp.CURRENCY_ID AS VARCHAR) = TRY_CAST(src.CURRENCY_ID AS VARCHAR)

),

    lkp_lkp_fxrate AS (
    SELECT
        src.*,
        lkp.FX_RATE AS FX_RATE
    FROM lkp_lkp_currency src
    LEFT JOIN {{ source('dbo', 'ref_fx_rate') }} lkp
        ON TRY_CAST(lkp.FX_RATE_ID AS VARCHAR) = TRY_CAST(src.FX_RATE_ID AS VARCHAR)

)

SELECT
    TXN_ID AS TXN_ID,
    CUST_NAME AS CUST_NAME,
    REGION_NAME AS REGION_NAME,
    COUNTRY_NAME AS COUNTRY_NAME,
    CURRENCY_CODE AS CURRENCY_CODE,
    FX_RATE AS FX_RATE
FROM lkp_lkp_fxrate

