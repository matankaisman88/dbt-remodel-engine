-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_clean_names"
  )
}}
-- Target: TGT_CLEAN_NAMES
-- Informatica Load Order: 1
-- Source Instances: SRC_RAW_NAMES
WITH
    sq_sq_raw_names AS (
SELECT FULL_NAME FROM {{ source('dbo', 'src_raw_names') }}
),

    map_mp_outer_inst_bind AS (
    SELECT
        FULL_NAME AS STR
    FROM sq_sq_raw_names

),

    map_mp_outer_inst__mp_inner_inst__bind AS (
    SELECT
        STR AS STR_IN,
        STR AS STR
    FROM map_mp_outer_inst_bind

),

    map_mp_outer_inst__mp_inner_inst__exp_trim AS (
    SELECT
        *,
        ltrim(rtrim(STR_IN)) AS STR_OUT
    FROM map_mp_outer_inst__mp_inner_inst__bind base

),

    int_mp_outer_inst__mp_inner_inst AS (
    SELECT
        STR_OUT AS STR
    FROM map_mp_outer_inst__mp_inner_inst__exp_trim

),

    map_mp_outer_inst_exp_upper_bind AS (
    SELECT
        STR AS STR_IN
    FROM int_mp_outer_inst__mp_inner_inst

),

    map_mp_outer_inst_exp_upper AS (
    SELECT
        *,
        upper(STR_IN) AS STR_OUT
    FROM map_mp_outer_inst_exp_upper_bind base

),

    int_mp_outer_inst AS (
    SELECT
        STR_OUT AS STR
    FROM map_mp_outer_inst_exp_upper

)

SELECT
    STR AS FULL_NAME
FROM int_mp_outer_inst

