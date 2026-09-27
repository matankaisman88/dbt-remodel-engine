-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_lnd_open_subscription_detail"
  )
}}
-- Target: TGT_LND_OPEN_SUBSCRIPTION_DETAIL
-- Informatica Load Order: 1
-- Source Instances: SRC_EXT_CDC_SUBSCRIPTION_EVENTS
WITH
    sq_sq_ext_cdc AS (
SELECT RECORD_ID, AUTO_EXPORT_BATCH_ID, ACTION, TX_TIMESTAMP FROM {{ source('cdc', 'src_ext_cdc_subscription_events') }} WHERE TX_TIMESTAMP >= CAST('{{ var('LastDeltaWatermark') }}' AS TIMESTAMP)
),

    int_exp_delta AS (
    SELECT
        base.RECORD_ID,
        base.AUTO_EXPORT_BATCH_ID,
        base.TX_TIMESTAMP,
        upper(ACTION) AS ACTION
    FROM sq_sq_ext_cdc base

)

SELECT
    RECORD_ID AS RECORD_ID,
    AUTO_EXPORT_BATCH_ID AS AUTO_EXPORT_BATCH_ID,
    ACTION AS ACTION,
    TX_TIMESTAMP AS TX_TIMESTAMP
FROM int_exp_delta

