-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "dw_core_tmp_staging_events_clean"
  )
}}
-- Target: dw_core_tmp_staging_events_clean
-- Informatica Load Order: 1
-- Source Instances: legacy_ops_tmp_staging_raw_events
WITH
    sq_sq_legacy_ops_tmp_staging_raw_events AS (
SELECT EVENT_KEY, PAYLOAD, STATUS FROM {{ source('legacy_ops_tmp', 'staging_raw_events') }}
),

    int_fil_valid AS (
    SELECT
        base.*
    FROM sq_sq_legacy_ops_tmp_staging_raw_events base
    WHERE STATUS = 'VALID'

)

SELECT
    EVENT_KEY AS EVENT_KEY,
    PAYLOAD AS PAYLOAD,
    STATUS AS STATUS
FROM int_fil_valid

