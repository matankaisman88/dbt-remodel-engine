-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_leaderboard_sorted"
  )
}}
-- Target: TGT_LEADERBOARD_SORTED
-- Informatica Load Order: 1
-- Source Instances: SRC_LEADERBOARD
WITH
    sq_sq_leaderboard AS (
SELECT PLAYER, SCORE, LEVEL, TIMESTAMP_COL FROM {{ source('dbo', 'src_leaderboard') }}
),

    int_srt_leaderboard AS (
    SELECT *
    FROM sq_sq_leaderboard

)

SELECT
    PLAYER AS PLAYER,
    SCORE AS SCORE,
    LEVEL AS LEVEL,
    TIMESTAMP_COL AS TIMESTAMP_COL
FROM int_srt_leaderboard

