-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_clean_labels"
  )
}}
-- Target: TGT_CLEAN_LABELS
-- Informatica Load Order: 1
-- Source Instances: SRC_RAW_LABELS
WITH
    sq_sq_raw_labels AS (
SELECT LABEL_TEXT FROM {{ source('dbo', 'src_raw_labels') }}
),

    map_mp_trim_inst_bind AS (
    SELECT
        LABEL_TEXT AS STR_IN,
        LABEL_TEXT AS STR
    FROM sq_sq_raw_labels

),

    map_mp_trim_inst_exp_trim AS (
    SELECT
        *,
        ltrim(rtrim(STR_IN)) AS STR_OUT
    FROM map_mp_trim_inst_bind base

),

    int_mp_trim_inst AS (
    SELECT
        STR_OUT AS STR
    FROM map_mp_trim_inst_exp_trim

),

    map_mp_uppercase2_inst_bind AS (
    SELECT
        STR AS STR_IN,
        STR AS STR
    FROM int_mp_trim_inst

),

    map_mp_uppercase2_inst_exp_upper2 AS (
    SELECT
        *,
        upper(STR_IN) AS STR_OUT
    FROM map_mp_uppercase2_inst_bind base

),

    int_mp_uppercase2_inst AS (
    SELECT
        STR_OUT AS STR
    FROM map_mp_uppercase2_inst_exp_upper2

)

SELECT
    STR AS LABEL_TEXT
FROM int_mp_uppercase2_inst

