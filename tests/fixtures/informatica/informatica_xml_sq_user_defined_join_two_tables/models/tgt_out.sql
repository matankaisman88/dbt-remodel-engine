-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_out"
  )
}}
-- Target: TGT_OUT
-- Informatica Load Order: 1
-- Source Instances: SRC_DETAIL, SRC_SUBSCRIPTION_MASTER
WITH
    sq_sq_src_detail AS (
    SELECT *
    FROM {{ source('billing_landing', 'src_detail') }} AS SRC_DETAIL
    INNER JOIN {{ source('billing_landing', 'src_subscription_master') }} AS SRC_SUBSCRIPTION_MASTER
    ON SRC_DETAIL.RECORD_ID = SRC_SUBSCRIPTION_MASTER.RECORD_ID AND SRC_DETAIL.AUTO_EXPORT_BATCH_ID = SRC_SUBSCRIPTION_MASTER.MASTER_AUTO_EXPORT_BATCH_ID

)

SELECT
    RECORD_ID AS RECORD_ID
FROM sq_sq_src_detail

