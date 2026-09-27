-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_log_processed"
  )
}}
-- Target: TGT_LOG_PROCESSED
-- Informatica Load Order: 1
-- Source Instances: SRC_RAW_LOG
WITH
    sq_sq_raw_log AS (
SELECT LOG_ID, RAW_MSG, SEVERITY, TS FROM {{ source('dbo', 'src_raw_log') }}
),

    int_exp_clean1 AS (
    SELECT
        base.*,
        LOG_ID AS LOG_ID_1,
        ltrim(rtrim(RAW_MSG)) AS MSG_1,
        SEVERITY AS SEVERITY_1,
        TS AS TS_1
    FROM sq_sq_raw_log base

),

    int_fil_not_debug AS (
    SELECT
        base.*
    FROM int_exp_clean1 base
    WHERE SEVERITY_1 != 'DEBUG'

),

    lkp_lkp_severity_code AS (
    SELECT
        src.*,
        lkp.LOG_ID_1 AS LOG_ID_1,
        lkp.MSG_1 AS MSG_1,
        lkp.TS_1 AS TS_1,
        lkp.SEVERITY_CODE AS SEVERITY_CODE
    FROM int_fil_not_debug src
    LEFT JOIN {{ source('dbo', 'ref_severity') }} lkp
        ON 1 = 1

),

    int_exp_clean2 AS (
    SELECT
        base.*,
        LOG_ID_1 AS LOG_ID_1_2,
        MSG_1 AS MSG_1_2,
        SEVERITY_1 AS SEVERITY_1_2,
        TS_1 AS TS_1_2,
        SEVERITY_CODE AS SEVERITY_CODE_2
    FROM lkp_lkp_severity_code base

),

    int_rtr_sev AS (
    SELECT
        *
    FROM int_exp_clean2 base

),

    int_exp_tag_critical AS (
    SELECT
        base.*,
        LOG_ID_1_2 AS LOG_ID_1_2_c,
        MSG_1_2 AS MSG_1_2_c,
        SEVERITY_1_2 AS SEVERITY_1_2_c,
        TS_1_2 AS TS_1_2_c,
        SEVERITY_CODE_2 AS SEVERITY_CODE_2_c,
        'Y' AS IS_CRIT
    FROM int_rtr_sev base

),

    int_exp_tag_normal AS (
    SELECT
        base.*,
        LOG_ID_1_2 AS LOG_ID_1_2_n,
        MSG_1_2 AS MSG_1_2_n,
        SEVERITY_1_2 AS SEVERITY_1_2_n,
        TS_1_2 AS TS_1_2_n,
        SEVERITY_CODE_2 AS SEVERITY_CODE_2_n,
        'N' AS IS_CRIT
    FROM int_rtr_sev base

),

    int_un_tagged AS (
    SELECT
        LOG_ID_1_2_c,
        MSG_1_2_c,
        SEVERITY_1_2_c,
        TS_1_2_c,
        SEVERITY_CODE_2_c,
        IS_CRIT
    FROM int_exp_tag_critical
    UNION ALL
    SELECT
        LOG_ID_1_2_n AS LOG_ID_1_2_c,
        MSG_1_2_n AS MSG_1_2_c,
        SEVERITY_1_2_n AS SEVERITY_1_2_c,
        TS_1_2_n AS TS_1_2_c,
        SEVERITY_CODE_2_n AS SEVERITY_CODE_2_c,
        IS_CRIT
    FROM int_exp_tag_normal

),

    int_srt_final AS (
    SELECT *
    FROM int_un_tagged

)

SELECT
    LOG_ID_1_2_c AS LOG_ID_1_2_c,
    MSG_1_2_c AS MSG_1_2_c,
    SEVERITY_1_2_c AS SEVERITY_1_2_c,
    TS_1_2_c AS TS_1_2_c,
    SEVERITY_CODE_2_c AS SEVERITY_CODE_2_c,
    IS_CRIT AS IS_CRIT
FROM int_srt_final

