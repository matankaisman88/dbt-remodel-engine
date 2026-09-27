-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'incremental',
    incremental_strategy = 'append',
    unique_key = 'SUBSCRIPTION_SUBSCRIPTION_EVENT_KEY',
    schema = "dbo",
    alias = "tgt_fct_subscription_lifecycle"
  )
}}
-- Target: TGT_FCT_SUBSCRIPTION_LIFECYCLE
-- Informatica Load Order: 1
-- Source Instances: SRC_STG_SUBSCRIPTION_LIFECYCLE
WITH
    sq_sq_stg AS (
SELECT SUBSCRIPTION_SUBSCRIPTION_EVENT_KEY, RATE_PLAN_CODE, ACCOUNT_ID, SUBSCRIPTION_LOG_DATE FROM {{ source('billing_core', 'stg_subscription_lifecycle') }}
),

    int_exp_fct AS (
    SELECT
        base.*,
        {{ var('BatchId') }} AS load_batch_id
    FROM sq_sq_stg base

),

    int_upd_fct AS (
    SELECT
        *,
        'I' AS informatica_update_action
    FROM int_exp_fct

)

SELECT
    SUBSCRIPTION_SUBSCRIPTION_EVENT_KEY AS SUBSCRIPTION_SUBSCRIPTION_EVENT_KEY,
    RATE_PLAN_CODE AS RATE_PLAN_CODE,
    ACCOUNT_ID AS ACCOUNT_ID,
    SUBSCRIPTION_LOG_DATE AS SUBSCRIPTION_LOG_DATE,
    load_batch_id AS load_batch_id
FROM int_upd_fct
{% if is_incremental() %}
WHERE SUBSCRIPTION_LOG_DATE > (SELECT coalesce(max(SUBSCRIPTION_LOG_DATE), '1900-01-01') FROM {{ this }})
   OR SUBSCRIPTION_SUBSCRIPTION_EVENT_KEY NOT IN (SELECT SUBSCRIPTION_SUBSCRIPTION_EVENT_KEY FROM {{ this }})
{% endif %}

