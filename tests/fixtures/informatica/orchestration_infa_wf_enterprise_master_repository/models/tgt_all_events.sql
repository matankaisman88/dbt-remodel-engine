-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_all_events"
  )
}}
-- Target: TGT_ALL_EVENTS
-- Informatica Load Order: 1
-- Source Instances: SRC_CALLCENTER_EVENTS, SRC_MOBILE_EVENTS, SRC_POS_EVENTS, SRC_WEB_EVENTS
WITH
    sq_sq_src_callcenter_events AS (
SELECT EVENT_ID, EVENT_TS, CHANNEL FROM {{ source('dbo', 'src_callcenter_events') }}
),

    sq_sq_src_mobile_events AS (
SELECT EVENT_ID, EVENT_TS, CHANNEL FROM {{ source('dbo', 'src_mobile_events') }}
),

    sq_sq_src_pos_events AS (
SELECT EVENT_ID, EVENT_TS, CHANNEL FROM {{ source('dbo', 'src_pos_events') }}
),

    sq_sq_src_web_events AS (
SELECT EVENT_ID, EVENT_TS, CHANNEL FROM {{ source('dbo', 'src_web_events') }}
),

    int_un_all_events AS (
    SELECT
        EVENT_ID,
        EVENT_TS,
        CHANNEL
    FROM sq_sq_src_web_events
    UNION ALL
    SELECT
        EVENT_ID,
        EVENT_TS,
        CHANNEL
    FROM sq_sq_src_mobile_events
    UNION ALL
    SELECT
        EVENT_ID,
        EVENT_TS,
        CHANNEL
    FROM sq_sq_src_pos_events
    UNION ALL
    SELECT
        EVENT_ID,
        EVENT_TS,
        CHANNEL
    FROM sq_sq_src_callcenter_events

)

SELECT
    EVENT_ID AS EVENT_ID,
    EVENT_TS AS EVENT_TS,
    CHANNEL AS CHANNEL
FROM int_un_all_events

