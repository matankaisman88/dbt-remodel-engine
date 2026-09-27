-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "stg_subscription_key"
  )
}}
-- Target: Shortcut_to_STG_SUBSCRIPTION_KEY
-- Informatica Load Order: 1
-- Source Instances: REF_DIM_RATE_PLAN, SRC_BILLING_AUDIT_TRAIL, Shortcut_to_SRC_OPEN_SUBSCRIPTION_DETAIL, Shortcut_to_SRC_SUBSCRIPTION_MASTER, Shortcut_to_SRC_SUBSCRIPTION_MASTER1, Shortcut_to_SRC_SUBSCRIPTION_MASTER2, Shortcut_to_SRC_TERMINATED_SUBSCRIPTION_DETAIL
WITH
    sq_sq_ref_dim_rate_plan AS (
    -- MANUAL_REVIEW_REQUIRED: mapping-level User Defined Join present on this Source Qualifier
    -- and not compiled into this query. Joined source table(s) not reflected in the SELECT below:
    -- billing_landing.src_billing_audit_trail. Original join predicate: ref_billing.core_core_dbo.REF_DIM_RATE_PLAN. RATE_PLAN_CODE_ENG_DESC= LTRIM(RTRIM(SRC_BILLING_AUDIT_TRAIL.OPERATION)) OR LTRIM(RTRIM(SRC_BILLING_AUDIT_TRAIL .OPERATION))= ref_billing.core_core_dbo.REF_DIM_RATE_PLAN.RATE_PLAN_DESC.
    -- joined source not compiled into SELECT: {{ source('billing_landing', 'src_billing_audit_trail') }}
    SELECT *
    FROM {{ source('dbo', 'ref_dim_rate_plan') }}

),

    int_exptrans1 AS (
    SELECT
        base.*
    FROM sq_sq_ref_dim_rate_plan base

),

    int_rnktrans AS (
    SELECT *
    FROM (
        SELECT
        ROW_NUMBER() OVER (PARTITION BY base.RATE_PLAN_PK, base.RECORD_ID, base.LINE ORDER BY base.END_DATE DESC) AS RANKINDEX,
        base.RATE_PLAN_CODE_Y,
        base.RATE_PLAN_PK,
        base.END_DATE,
        base.RECORD_ID,
        base.AUTO_EXPORT_BATCH_ID,
        base.OFFSET,
        base.LOG_DATE,
        base.LINE
        FROM int_exptrans1 base
    ) ranked
    WHERE RANKINDEX <= 1

),

    int_srttrans AS (
    SELECT *
    FROM int_rnktrans

),

    sq_sq_shortcut_to_src_open_subscription_detail AS (
    SELECT *
    FROM {{ source('billing_landing', 'src_open_subscription_detail') }} AS SRC_OPEN_SUBSCRIPTION_DETAIL
    INNER JOIN {{ source('billing_landing', 'src_subscription_master') }} AS SRC_SUBSCRIPTION_MASTER
    ON SRC_OPEN_SUBSCRIPTION_DETAIL.RECORD_ID = SRC_SUBSCRIPTION_MASTER.RECORD_ID AND SRC_OPEN_SUBSCRIPTION_DETAIL.AUTO_EXPORT_BATCH_ID = SRC_SUBSCRIPTION_MASTER.MASTER_AUTO_EXPORT_BATCH_ID

),

    int_exp_src_subscription_detail AS (
    SELECT
        base.*,
        REPLACE(upper('SRC_OPEN_SUBSCRIPTION_DETAIL'), 'SHORTCUT_TO_', COALESCE(NULL, '')) AS SOURCE_TABLE,
        CAST(strptime('31/12/2999', '%d/%m/%Y') AS DATE) AS STOP_DATE
    FROM sq_sq_shortcut_to_src_open_subscription_detail base

),

    sq_sq_src_billing_audit_trail AS (
    SELECT *
    FROM {{ source('billing_landing', 'src_billing_audit_trail') }} AS SRC_BILLING_AUDIT_TRAIL
    INNER JOIN {{ source('billing_landing', 'src_subscription_master') }} AS SRC_SUBSCRIPTION_MASTER
    ON SRC_BILLING_AUDIT_TRAIL.RECORD_ID = SRC_SUBSCRIPTION_MASTER.RECORD_ID AND SRC_BILLING_AUDIT_TRAIL.AUTO_EXPORT_BATCH_ID = SRC_SUBSCRIPTION_MASTER.MASTER_AUTO_EXPORT_BATCH_ID

),

    int_exptrans AS (
    SELECT
        base.*,
        'SRC_BILLING_AUDIT_TRAIL' AS SOURCE_TABLE,
        CAST(strptime('31/12/2999', '%d/%m/%Y') AS DATE) AS STOP_DATE,
        ltrim(rtrim(OPERATION)) AS OPERATION_out
    FROM sq_sq_src_billing_audit_trail base

),

    int_srttrans1 AS (
    SELECT *
    FROM int_exptrans

),

    int_jnrtrans AS (
    SELECT
        d.RATE_PLAN_CODE_Y,
        d.RECORD_ID,
        d.AUTO_EXPORT_BATCH_ID,
        d.OFFSET,
        d.LOG_DATE,
        m.RECORD_ID AS RECORD_ID1,
        m.AUTO_EXPORT_BATCH_ID AS AUTO_EXPORT_BATCH_ID1,
        m.OFFSET AS OFFSET1,
        m.LOG_DATE AS LOG_DATE1,
        m.RECORD_CREATED_AT,
        m.ACCOUNT_REF_CODE,
        m.CSR_EXT_AGENT_NUM,
        m.CSR_EXT_ROLE_CODE,
        m.LINE,
        m.TRANSACTION_ID,
        m.ACTION,
        m.MASTER_AUTO_EXPORT_BATCH_ID,
        m.SOURCE_TABLE,
        m.CREATED_BY_USER_ID,
        m.BILLING_LOCATION_CODE,
        m.PRODUCT_LINE_CODE,
        m.BILLING_ENTITY_NAME,
        m.BILLING_ENTITY_CODE,
        m.REMARK,
        m.STOP_DATE,
        m.CSR_AGENT_IDENTITY,
        m.OPERATION,
        m.OPERATION_out,
        d.LINE AS LINE1,
        d.RATE_PLAN_PK,
        m.SERVICE_ACTIVATION_DATE
    FROM int_srttrans1 m
    RIGHT JOIN int_srttrans d
        ON m.RECORD_ID = d.RECORD_ID AND m.AUTO_EXPORT_BATCH_ID = d.AUTO_EXPORT_BATCH_ID AND m.OFFSET = d.OFFSET AND m.LOG_DATE = d.LOG_DATE AND m.LINE = d.LINE

),

    lkp_lkp_ref_rate_plan_aliases AS (
    SELECT *
    FROM (
        SELECT
            src.*,
        lkp.RATE_PLAN_CODE AS RATE_PLAN_CODE,
        lkp.RATE_PLAN_DESC AS RATE_PLAN_DESC,
            ROW_NUMBER() OVER (PARTITION BY src.OPERATION_out ORDER BY 1) AS rn
        FROM int_jnrtrans src
        LEFT JOIN {{ source('dwh', 'ref_rate_plan_aliases') }} lkp
            ON TRY_CAST(lkp.RATE_PLAN_DESC AS VARCHAR) = TRY_CAST(src.OPERATION_out AS VARCHAR)
    ) deduped
    WHERE rn = 1

),

    int_exptrans2_bind AS (
    SELECT
        base.RATE_PLAN_PK AS RATE_PLAN_PK_dim_classification,
        u0.RATE_PLAN_CODE AS RATE_PLAN_CODE,
        u0.RATE_PLAN_CODE_Y AS RATE_PLAN_CODE_Y,
        base.*
    FROM int_jnrtrans base
    LEFT JOIN lkp_lkp_ref_rate_plan_aliases u0 ON base.OPERATION_out = u0.OPERATION_out

),

    int_exptrans2 AS (
    SELECT
        *,
        COALESCE(RATE_PLAN_CODE_Y, RATE_PLAN_CODE) AS RATE_PLAN_CODE_out
    FROM int_exptrans2_bind base

),

    sq_sq_shortcut_to_src_terminated_subscription_detail AS (
    SELECT *
    FROM {{ source('billing_landing', 'src_terminated_subscription_detail') }} AS SRC_TERMINATED_SUBSCRIPTION_DETAIL
    INNER JOIN {{ source('billing_landing', 'src_subscription_master') }} AS SRC_SUBSCRIPTION_MASTER
    ON SRC_TERMINATED_SUBSCRIPTION_DETAIL.RECORD_ID = SRC_SUBSCRIPTION_MASTER.RECORD_ID AND SRC_TERMINATED_SUBSCRIPTION_DETAIL.AUTO_EXPORT_BATCH_ID = SRC_SUBSCRIPTION_MASTER.MASTER_AUTO_EXPORT_BATCH_ID

),

    int_exp_src_subscription_detail1_bind AS (
    SELECT
        base.CSR_AGENT_NAME AS CSR_AGENT_NAME,
        base.CSR_AGENT_ID AS CSR_AGENT_ID,
        base.CREATED_BY_USER_ID AS CREATED_BY_USER_ID,
        base.RECORD_CREATED_AT AS RECORD_CREATED_AT,
        base.RECORD_ID AS RECORD_ID,
        base.ACTION AS ACTION,
        base.MASTER_AUTO_EXPORT_BATCH_ID AS MASTER_AUTO_EXPORT_BATCH_ID,
        base.SERVICE_ACTIVATION_DATE AS SERVICE_START_RAW,
        base.RATE_PLAN AS RATE_PLAN,
        base.BILLING_ENTITY_CODE AS BILLING_ENTITY_CODE,
        base.BILLING_ENTITY_NAME AS BILLING_ENTITY_NAME,
        base.TRANSACTION_ID AS TRANSACTION_ID,
        base.STOP_REASON AS STOP_REASON,
        base.TX_TIMESTAMP AS TX_TIMESTAMP,
        base.CLOSED_BY AS CLOSED_BY,
        base.STOP_DATE AS STOP_DATE,
        base.CODE AS CODE,
        base.CHARACTERISTIC2 AS CHARACTERISTIC2,
        base.CHARACTERISTIC1 AS CHARACTERISTIC1,
        base.NOTE AS NOTE,
        base.LINE AS LINE,
        base.CSR_EXT_ROLE_CODE AS CSR_EXT_ROLE_CODE,
        base.CSR_EXT_AGENT_NUM AS CSR_EXT_AGENT_NUM,
        base.ACCOUNT_REF_CODE AS ACCOUNT_REF_CODE,
        base.BILLING_LOCATION_CODE AS BILLING_LOCATION_CODE,
        base.MARKET_SEGMENT_NAME AS MARKET_SEGMENT_NAME,
        base.MARKET_SEGMENT_CODE AS MARKET_SEGMENT_CODE,
        base.*
    FROM sq_sq_shortcut_to_src_terminated_subscription_detail base

),

    int_exp_src_subscription_detail1 AS (
    SELECT
        base.*,
        REPLACE(upper('SRC_TERMINATED_SUBSCRIPTION_DETAIL'), 'SHORTCUT_TO_', COALESCE(NULL, '')) AS SOURCE_TABLE
    FROM int_exp_src_subscription_detail1_bind base

),

    int_union1 AS (
    SELECT
        RECORD_ID AS RECORD_ID,
        RECORD_CREATED_AT AS RECORD_CREATED_AT,
        ACCOUNT_REF_CODE AS ACCOUNT_REF_CODE,
        CSR_EXT_AGENT_NUM AS CSR_EXT_AGENT_NUM,
        CSR_EXT_ROLE_CODE AS CSR_EXT_ROLE_CODE,
        LINE AS LINE,
        CODE AS CODE,
        CHARACTERISTIC1 AS CHARACTERISTIC1,
        CHARACTERISTIC2 AS CHARACTERISTIC2,
        NOTE AS NOTE,
        TX_TIMESTAMP AS TX_TIMESTAMP,
        SERVICE_START_RAW AS SERVICE_START_RAW,
        STOP_DATE AS STOP_DATE,
        NULL AS STOP_REASON,
        TRANSACTION_ID AS TRANSACTION_ID,
        MASTER_AUTO_EXPORT_BATCH_ID AS MASTER_AUTO_EXPORT_BATCH_ID,
        ACTION AS ACTION,
        SOURCE_TABLE AS SOURCE_TABLE,
        CREATED_BY_USER_ID AS CREATED_BY_USER_ID,
        BILLING_LOCATION_CODE AS BILLING_LOCATION_CODE,
        CSR_AGENT_ID AS CSR_AGENT_ID,
        CSR_AGENT_NAME AS CSR_AGENT_NAME,
        MARKET_SEGMENT_NAME AS MARKET_SEGMENT_NAME,
        MARKET_SEGMENT_CODE AS MARKET_SEGMENT_CODE,
        NULL AS CLOSED_BY,
        NULL AS LOG_DATE,
        BILLING_ENTITY_NAME AS BILLING_ENTITY_NAME,
        BILLING_ENTITY_CODE AS BILLING_ENTITY_CODE,
        RATE_PLAN AS RATE_PLAN,
        NULL AS RATE_PLAN_PK
    FROM int_exp_src_subscription_detail
    UNION ALL
    SELECT
        RECORD_ID AS RECORD_ID,
        RECORD_CREATED_AT AS RECORD_CREATED_AT,
        ACCOUNT_REF_CODE AS ACCOUNT_REF_CODE,
        CSR_EXT_AGENT_NUM AS CSR_EXT_AGENT_NUM,
        CSR_EXT_ROLE_CODE AS CSR_EXT_ROLE_CODE,
        LINE AS LINE,
        CODE AS CODE,
        CHARACTERISTIC1 AS CHARACTERISTIC1,
        CHARACTERISTIC2 AS CHARACTERISTIC2,
        NOTE AS NOTE,
        TX_TIMESTAMP AS TX_TIMESTAMP,
        SERVICE_START_RAW AS SERVICE_START_RAW,
        STOP_DATE AS STOP_DATE,
        STOP_REASON AS STOP_REASON,
        TRANSACTION_ID AS TRANSACTION_ID,
        MASTER_AUTO_EXPORT_BATCH_ID AS MASTER_AUTO_EXPORT_BATCH_ID,
        ACTION AS ACTION,
        SOURCE_TABLE AS SOURCE_TABLE,
        CREATED_BY_USER_ID AS CREATED_BY_USER_ID,
        BILLING_LOCATION_CODE AS BILLING_LOCATION_CODE,
        CSR_AGENT_ID AS CSR_AGENT_ID,
        CSR_AGENT_NAME AS CSR_AGENT_NAME,
        MARKET_SEGMENT_NAME AS MARKET_SEGMENT_NAME,
        MARKET_SEGMENT_CODE AS MARKET_SEGMENT_CODE,
        CLOSED_BY AS CLOSED_BY,
        NULL AS LOG_DATE,
        BILLING_ENTITY_NAME AS BILLING_ENTITY_NAME,
        BILLING_ENTITY_CODE AS BILLING_ENTITY_CODE,
        RATE_PLAN AS RATE_PLAN,
        NULL AS RATE_PLAN_PK
    FROM int_exp_src_subscription_detail1
    UNION ALL
    SELECT
        RECORD_ID1 AS RECORD_ID,
        RECORD_CREATED_AT AS RECORD_CREATED_AT,
        ACCOUNT_REF_CODE AS ACCOUNT_REF_CODE,
        CSR_EXT_AGENT_NUM AS CSR_EXT_AGENT_NUM,
        CSR_EXT_ROLE_CODE AS CSR_EXT_ROLE_CODE,
        LINE AS LINE,
        RATE_PLAN_CODE_out AS CODE,
        NULL AS CHARACTERISTIC1,
        NULL AS CHARACTERISTIC2,
        REMARK AS NOTE,
        LOG_DATE1 AS TX_TIMESTAMP,
        SERVICE_ACTIVATION_DATE AS SERVICE_START_RAW,
        STOP_DATE AS STOP_DATE,
        NULL AS STOP_REASON,
        TRANSACTION_ID AS TRANSACTION_ID,
        MASTER_AUTO_EXPORT_BATCH_ID AS MASTER_AUTO_EXPORT_BATCH_ID,
        ACTION AS ACTION,
        SOURCE_TABLE AS SOURCE_TABLE,
        CREATED_BY_USER_ID AS CREATED_BY_USER_ID,
        BILLING_LOCATION_CODE AS BILLING_LOCATION_CODE,
        CSR_AGENT_IDENTITY AS CSR_AGENT_ID,
        NULL AS CSR_AGENT_NAME,
        NULL AS MARKET_SEGMENT_NAME,
        PRODUCT_LINE_CODE AS MARKET_SEGMENT_CODE,
        NULL AS CLOSED_BY,
        LOG_DATE1 AS LOG_DATE,
        BILLING_ENTITY_NAME AS BILLING_ENTITY_NAME,
        BILLING_ENTITY_CODE AS BILLING_ENTITY_CODE,
        OPERATION AS RATE_PLAN,
        RATE_PLAN_PK_dim_classification AS RATE_PLAN_PK
    FROM int_exptrans2

),

    int_exp_cast_to_int_bind AS (
    SELECT
        base.CSR_EXT_AGENT_NUM AS CSR_EXT_AGENT_NUM,
        base.CSR_EXT_ROLE_CODE AS CSR_EXT_ROLE_CODE,
        base.CREATED_BY_USER_ID AS CREATED_BY_USER_ID,
        base.BILLING_LOCATION_CODE AS BILLING_LOCATION_CODE,
        base.MARKET_SEGMENT_CODE AS MARKET_SEGMENT_CODE_in,
        base.RECORD_CREATED_AT AS RECORD_CREATED_AT,
        base.*
    FROM int_union1 base

),

    int_exp_cast_to_int AS (
    SELECT
        *,
        CAST(RECORD_CREATED_AT AS DATE) AS RECORD_CREATED_AT_trunc,
        TRY_CAST(CSR_EXT_AGENT_NUM AS INT) AS CSR_EXT_AGENT_NUM_out,
        TRY_CAST(CSR_EXT_ROLE_CODE AS INT) AS CSR_EXT_ROLE_CODE_out,
        TRY_CAST(CREATED_BY_USER_ID AS INT) AS CREATED_BY_USER_ID_out,
        TRY_CAST(BILLING_LOCATION_CODE AS INT) AS BILLING_LOCATION_CODE_out,
        ltrim(MARKET_SEGMENT_CODE_in, '0') AS MARKET_SEGMENT_CODE
    FROM int_exp_cast_to_int_bind base

),

    lkp_lkp_ref_billing_region AS (
    SELECT *
    FROM (
        SELECT
            src.*,
        lkp.MANDT AS MANDT,
        lkp.PLVAR AS PLVAR,
        lkp.OTYPE AS OTYPE,
        lkp.OBJID AS OBJID,
        lkp.SUBTY AS SUBTY,
        lkp.ISTAT AS ISTAT,
        lkp.BEGDA AS BEGDA,
        lkp.ENDDA AS ENDDA,
        lkp.VARYF AS VARYF,
        lkp.SEQNR AS SEQNR,
        lkp.INFTY AS INFTY,
        lkp.OTJID AS OTJID,
        lkp.AEDTM AS AEDTM,
        lkp.UNAME AS UNAME,
        lkp.REASN AS REASN,
        lkp.HISTO AS HISTO,
        lkp.ITXNR AS ITXNR,
        lkp.TR_TO_ZAKAUT AS TR_TO_ZAKAUT,
        lkp.ZAKAUT_PERIOD AS ZAKAUT_PERIOD,
        lkp.INCLUD_DOC_PATNT AS INCLUD_DOC_PATNT,
        lkp.ACT_TERPST_CHECK AS ACT_TERPST_CHECK,
        lkp.HETEL_PRICE AS HETEL_PRICE,
        lkp.MAGNET_CARD_CODE AS MAGNET_CARD_CODE,
        lkp.AGREEM_TY_CODE AS AGREEM_TY_CODE,
        lkp.AGE_RANGE_FROM AS AGE_RANGE_FROM,
        lkp.AGE_RANGE_TO AS AGE_RANGE_TO,
        lkp.RESTRCTD_TO_GNDR AS RESTRCTD_TO_GNDR,
        lkp.FRST_VIS_CHECK AS FRST_VIS_CHECK,
        lkp.ACCEPTS_URGENT AS ACCEPTS_URGENT,
        lkp.SHIFT_NOT_MANDT AS SHIFT_NOT_MANDT,
        lkp.NOFIRST_VIS_CHK AS NOFIRST_VIS_CHK,
        lkp.APPRV_WO_EXAM AS APPRV_WO_EXAM,
        lkp.NORCRD_IN_APPVFL AS NORCRD_IN_APPVFL,
        lkp.SERVICE_IN_ENG AS SERVICE_IN_ENG,
        lkp.SERVICE_SHRT_NM AS SERVICE_SHRT_NM,
        lkp.SERVICE_LONG_NM AS SERVICE_LONG_NM,
        lkp.KNOWN_OCCUPATION AS KNOWN_OCCUPATION,
        lkp.KNOWNAS_OCPTN_AR AS KNOWNAS_OCPTN_AR,
        lkp.TYPE_OF_EXPERTS AS TYPE_OF_EXPERTS,
        lkp.AUTH_OBLGTD_TASK AS AUTH_OBLGTD_TASK,
        lkp.RELEVNT_POPULAT AS RELEVNT_POPULAT,
        lkp.REFERENCE_TYPE AS REFERENCE_TYPE,
        lkp.REFERRAL_ELEMENT AS REFERRAL_ELEMENT,
        lkp.MEDC_FILE_TYPE1 AS MEDC_FILE_TYPE1,
        lkp.MEDC_FILE_TYPE2 AS MEDC_FILE_TYPE2,
        lkp.HQ_IN_CHARGE_JOB AS HQ_IN_CHARGE_JOB,
        lkp.CNTY_IN_CHRG_JOB AS CNTY_IN_CHRG_JOB,
        lkp.PROF_CHARCT_RMRK AS PROF_CHARCT_RMRK,
        lkp.RELVNT_JOB_SEGEL AS RELVNT_JOB_SEGEL,
        lkp.CONVCODE_OLD_SHR AS CONVCODE_OLD_SHR,
        lkp.SPECIALIZTN_CODE AS SPECIALIZTN_CODE,
        lkp.PAYING_SYSTEM1 AS PAYING_SYSTEM1,
        lkp.PAYING_SYSTEM2 AS PAYING_SYSTEM2,
        lkp.PAYING_SYSTEM3 AS PAYING_SYSTEM3,
        lkp.LIMT_TO_EMP_GRP1 AS LIMT_TO_EMP_GRP1,
        lkp.LIMT_TO_EMP_GRP2 AS LIMT_TO_EMP_GRP2,
        lkp.NOT_IN_DIV_JOBGR AS NOT_IN_DIV_JOBGR,
        lkp.ADD_POPULAT_CHAR AS ADD_POPULAT_CHAR,
        lkp.SERVICE_CHAR AS SERVICE_CHAR,
        lkp.APPOINTMENT_CALL AS APPOINTMENT_CALL,
        lkp.APP_CALL_BEGDA AS APP_CALL_BEGDA,
        lkp.APP_CALL_ENDDA AS APP_CALL_ENDDA,
        lkp.NO_APPROVAL AS NO_APPROVAL,
        lkp.MEDC_FILETYPE1 AS MEDC_FILETYPE1,
        lkp.SPEC_CODE2 AS SPEC_CODE2,
        lkp.SPEC_CODE3 AS SPEC_CODE3,
        lkp.TERMINAL_ID AS TERMINAL_ID,
        lkp.HETEL_GROUP AS HETEL_GROUP,
        lkp.CODE_GROUP AS CODE_GROUP,
        lkp.RELVNT_JOB_JOIN AS RELVNT_JOB_JOIN,
        lkp.CLICKS_NAME AS CLICKS_NAME,
        lkp.NO_RATE_PLAN_REPORT AS NO_RATE_PLAN_REPORT,
        lkp.QUARTERLY_ASCRIPTION AS QUARTERLY_ASCRIPTION,
        lkp.BLOCKING_APPROACH AS BLOCKING_APPROACH,
            ROW_NUMBER() OVER (PARTITION BY src.MARKET_SEGMENT_CODE ORDER BY 1) AS rn
        FROM int_exp_cast_to_int src
        LEFT JOIN {{ source('dbo', 'ref_billing_region') }} lkp
            ON TRY_CAST(lkp.MAGNET_CARD_CODE AS VARCHAR) = TRY_CAST(src.MARKET_SEGMENT_CODE AS VARCHAR)
    ) deduped
    WHERE rn = 1

),

    int_exp_fields_bind AS (
    SELECT
        base.CSR_EXT_ROLE_CODE_out AS CSR_EXT_ROLE_CODE_in,
        base.RECORD_CREATED_AT_trunc AS SUBSCRIPTION_CREATE_DATE_trunc,
        base.CSR_EXT_AGENT_NUM_out AS CSR_EXT_AGENT_NUM_in,
        u0.OBJID AS OBJID,
        base.CHARACTERISTIC1 AS CHARACTERISTIC1_in,
        base.CODE AS CODE_in,
        base.LINE AS LINE_in,
        base.CSR_EXT_ROLE_CODE AS CSR_EXT_ROLE_ID_in,
        base.TX_TIMESTAMP AS TX_TIMESTAMP_in,
        base.RECORD_ID AS RECORD_ID_in,
        base.ACCOUNT_REF_CODE AS ACCOUNT_REF_CODE_in,
        base.ACTION AS ACTION_in,
        base.STOP_REASON AS STOP_REASON_in,
        base.STOP_DATE AS STOP_DATE_in,
        base.SERVICE_START_RAW AS SERVICE_START_RAW_in,
        base.NOTE AS NOTE_in,
        base.CHARACTERISTIC2 AS CHARACTERISTIC2_in,
        base.*
    FROM int_exp_cast_to_int base
    LEFT JOIN lkp_lkp_ref_billing_region u0 ON base.MARKET_SEGMENT_CODE = u0.MARKET_SEGMENT_CODE

),

    int_exp_fields_prep AS (
    SELECT
        base.*,
        CASE WHEN (TX_TIMESTAMP_in IS NOT NULL) THEN CAST(strptime(strftime(TRY_CAST(TX_TIMESTAMP_in AS TIMESTAMP), '%Y-%m') || '-01', '%Y-%m-%d') AS DATE) ELSE TX_TIMESTAMP_in END AS TX_TIMESTAMP_v,
        COALESCE(TX_TIMESTAMP_in, CAST(strptime('1900-01-01', '%Y-%m-%d') AS DATE)) AS SUBSCRIPTION_LOG_DATE_v,
        CASE WHEN length(SERVICE_START_RAW_in)=8 and  substr(SERVICE_START_RAW_in, 3, 2)='//' and (TRY_CAST(substr(SERVICE_START_RAW_in, 1, 2) AS NUMERIC) IS NOT NULL) AND TRY_CAST(substr(SERVICE_START_RAW_in, 1, 2) AS INT) >= 1 AND TRY_CAST(substr(SERVICE_START_RAW_in, 1, 2) AS INT) <= 12 and (TRY_CAST(substr(SERVICE_START_RAW_in, 5, 4) AS NUMERIC) IS NOT NULL) AND TRY_CAST(substr(SERVICE_START_RAW_in, 5, 4) AS INT) >= 1900 THEN '01/'||substr(SERVICE_START_RAW_in, 1, 2)||'/'|| substr(SERVICE_START_RAW_in, 5, 4) ELSE null END AS SERVICE_START_RAW_v1,
        CASE WHEN ( length(SERVICE_START_RAW_in) = 5 AND (TRY_CAST(SERVICE_START_RAW_in AS NUMERIC) IS NOT NULL) AND TRY_CAST(substr(SERVICE_START_RAW_in, 1, 1) AS INT) >= 1 AND TRY_CAST(substr(SERVICE_START_RAW_in, 1, 1) AS INT) <= 12 AND TRY_CAST(substr(SERVICE_START_RAW_in, 2, 4) AS INT) >= 1900 ) THEN '01/0'||substr(SERVICE_START_RAW_in, 1, 1)||'/'||substr(SERVICE_START_RAW_in, 2, 4) ELSE NULL END AS SERVICE_START_RAW_v2,
        CASE WHEN length(SERVICE_START_RAW_in) = 6 AND (TRY_CAST(SERVICE_START_RAW_in AS NUMERIC) IS NOT NULL) AND TRY_CAST(substr(SERVICE_START_RAW_in, 1, 2) AS INT) >= 1 AND TRY_CAST(substr(SERVICE_START_RAW_in, 1, 2) AS INT) <= 12 AND TRY_CAST(substr(SERVICE_START_RAW_in, 3, 4) AS INT) >= 1900 THEN '01/'||substr(SERVICE_START_RAW_in, 1, 2)||'/'||substr(SERVICE_START_RAW_in, 3, 4) ELSE NULL END AS SERVICE_START_RAW_v3,
        CASE WHEN (SERVICE_START_RAW_v1 IS NOT NULL) THEN SERVICE_START_RAW_v1 WHEN (SERVICE_START_RAW_v2 IS NOT NULL) THEN SERVICE_START_RAW_v2 WHEN (SERVICE_START_RAW_v3 IS NOT NULL) THEN SERVICE_START_RAW_v3 ELSE null END AS SERVICE_START_RAW_v,
        CASE WHEN (try_strptime(ltrim(rtrim(SERVICE_START_RAW_in)), '%y') IS NOT NULL) AND length(ltrim(rtrim(SERVICE_START_RAW_in))) = 2 THEN CASE WHEN TRY_CAST(ltrim(rtrim(SERVICE_START_RAW_in)) AS NUMERIC)  < 80 THEN '01/01/20' || ltrim(rtrim(SERVICE_START_RAW_in)) ELSE '01/01/19' || ltrim(rtrim(SERVICE_START_RAW_in)) END WHEN (try_strptime(ltrim(rtrim(SERVICE_START_RAW_in)), '%Y') IS NOT NULL) AND length(ltrim(rtrim(SERVICE_START_RAW_in))) = 4 THEN '01/01/' || ltrim(rtrim(SERVICE_START_RAW_in)) WHEN (try_strptime(ltrim(rtrim(SERVICE_START_RAW_in)), '%m/%y') IS NOT NULL) AND length(ltrim(rtrim(SERVICE_START_RAW_in))) = 5 THEN CASE WHEN TRY_CAST(substr(ltrim(rtrim(SERVICE_START_RAW_in)), 4) AS NUMERIC)  < 80 THEN '01/' || substr(ltrim(rtrim(SERVICE_START_RAW_in)), 1, 3) || '20' || substr(ltrim(rtrim(SERVICE_START_RAW_in)), 4) ELSE '01/' || substr(ltrim(rtrim(SERVICE_START_RAW_in)), 1, 3) || '19' || substr(ltrim(rtrim(SERVICE_START_RAW_in)), 4) END WHEN (try_strptime(ltrim(rtrim(SERVICE_START_RAW_in)), '%m/%Y') IS NOT NULL) AND length(ltrim(rtrim(SERVICE_START_RAW_in))) = 7 THEN '01/' || ltrim(rtrim(SERVICE_START_RAW_in)) WHEN (try_strptime(ltrim(rtrim(SERVICE_START_RAW_in)), '%d/%m/%y') IS NOT NULL) AND length(ltrim(rtrim(SERVICE_START_RAW_in))) = 8 THEN CASE WHEN TRY_CAST(substr(ltrim(rtrim(SERVICE_START_RAW_in)), 7) AS NUMERIC)  < 80 THEN substr(ltrim(rtrim(SERVICE_START_RAW_in)), 1, 6) || '20' || substr(ltrim(rtrim(SERVICE_START_RAW_in)), 7) ELSE substr(ltrim(rtrim(SERVICE_START_RAW_in)), 1, 6) || '19' || substr(ltrim(rtrim(SERVICE_START_RAW_in)), 7) END WHEN (try_strptime(ltrim(rtrim(SERVICE_START_RAW_in)), '%d/%m/%Y') IS NOT NULL) AND length(ltrim(rtrim(SERVICE_START_RAW_in))) = 10 THEN ltrim(rtrim(SERVICE_START_RAW_in)) ELSE NULL END AS SERVICE_BEGIN_DATE_v,
        CASE WHEN (SERVICE_BEGIN_DATE_v IS NULL) OR (try_strptime(SERVICE_BEGIN_DATE_v, '%d/%m/%Y') IS NULL) OR CAST(strptime(SERVICE_BEGIN_DATE_v, '%d/%m/%Y') AS DATE) < CAST(strptime('01/01/1900', '%d/%m/%Y') AS DATE) OR CAST(strptime(SERVICE_BEGIN_DATE_v, '%d/%m/%Y') AS DATE) = CAST(strptime('01/01/1900', '%d/%m/%Y') AS DATE) THEN TX_TIMESTAMP_v ELSE CAST(strptime(SERVICE_BEGIN_DATE_v, '%d/%m/%Y') AS DATE) END AS SERVICE_BEGIN_DATE,
        CASE WHEN SOURCE_TABLE='SRC_OPEN_SUBSCRIPTION_DETAIL' THEN SUBSCRIPTION_LOG_DATE_v WHEN SOURCE_TABLE='SRC_TERMINATED_SUBSCRIPTION_DETAIL' THEN STOP_DATE_in WHEN SOURCE_TABLE='SRC_BILLING_AUDIT_TRAIL' THEN LOG_DATE ELSE CAST(strptime('1900-01-01', '%Y-%m-%d') AS DATE) END AS DATE_v,
        'DATE' AS DATE_STR
    FROM int_exp_fields_bind base

),

    int_exp_fields AS (
    SELECT
        *,
        RECORD_ID_in AS SUBSCRIPTION_SUBSCRIPTION_EVENT_KEY,
        CASE WHEN length(ltrim(rtrim(ACCOUNT_REF_CODE_in))) = 10 THEN TRY_CAST(substr(ltrim(rtrim(ACCOUNT_REF_CODE_in)), 2) AS NUMERIC) ELSE TRY_CAST(ltrim(rtrim(ACCOUNT_REF_CODE_in)) AS NUMERIC) END AS ACCOUNT_ID,
        CASE WHEN length(ltrim(rtrim(ACCOUNT_REF_CODE_in))) = 10 THEN TRY_CAST(TRY_CAST(substr(ltrim(rtrim(ACCOUNT_REF_CODE_in)), 1, 1) AS NUMERIC) AS BIGINT) ELSE 0 END AS ACCOUNT_CODE,
        TRY_CAST(CSR_EXT_AGENT_NUM_in AS NUMERIC) AS CSR_NUMBER,
        TRY_CAST(CSR_EXT_ROLE_ID_in AS NUMERIC) AS CSR_ROLE_CODE,
        TRY_CAST(LINE_in AS NUMERIC) AS LINE_ITEM_NUM,
        COALESCE(CODE_in, '-1') AS RATE_PLAN_CODE,
        CHARACTERISTIC1_in AS RATING_ATTR1_CODE,
        CHARACTERISTIC2_in AS RATING_ATTR2_CODE,
        NOTE_in AS SUBSCRIPTION_EVENT_NOTE,
        CASE WHEN (SERVICE_START_RAW IS NOT NULL) THEN SERVICE_START_RAW WHEN (TX_TIMESTAMP_v IS NOT NULL) THEN TX_TIMESTAMP_v ELSE CAST(strptime('01/01/1900', '%d/%m/%Y') AS DATE) END AS SERVICE_START_RAW_out,
        SUBSCRIPTION_LOG_DATE_v AS SUBSCRIPTION_LOG_DATE,
        CASE WHEN (SERVICE_START_RAW_v IS NULL) THEN SERVICE_BEGIN_DATE ELSE CAST(strptime(SERVICE_START_RAW_v, '%d/%m/%Y') AS DATE) END AS SERVICE_BEGIN_DATE_out,
        STOP_DATE_in AS SERVICE_END_DATE,
        STOP_REASON_in AS SERVICE_END_REASON,
        upper(ltrim(rtrim(ACTION_in))) AS ACTION,
        CASE WHEN (TRY_CAST(CSR_AGENT_ID AS NUMERIC) IS NOT NULL) THEN TRY_CAST(CSR_AGENT_ID AS BIGINT) ELSE -1 END AS CSR_AGENT_ID_int,
        CASE WHEN (MARKET_SEGMENT_CODE IS NOT NULL) THEN MARKET_SEGMENT_CODE ELSE '-1' END AS o_MARKET_SEGMENT_CODE,
        COALESCE(DATE_v, CAST(strptime('1900-01-01', '%Y-%m-%d') AS DATE)) AS DATE_out,
        CASE WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%d/%m/%Y') IS NOT NULL) AND length(ltrim(rtrim(DATE_STR))) = 10 AND substr(ltrim(rtrim(DATE_STR)), 3, 1) ='.' AND substr(ltrim(rtrim(DATE_STR)), 6, 1) ='.' THEN substr(ltrim(rtrim(DATE_STR)), 1, 2) ||'.' ||substr(ltrim(rtrim(DATE_STR)), 4, 2)  || '.' ||substr(ltrim(rtrim(DATE_STR)), 7) WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%d/%m/%y') IS NOT NULL)  AND length(ltrim(rtrim(DATE_STR))) = 8 AND substr(ltrim(rtrim(DATE_STR)), 3, 1) ='.' AND substr(ltrim(rtrim(DATE_STR)), 6, 1) ='.' THEN CASE WHEN TRY_CAST(substr(ltrim(rtrim(DATE_STR)), 7) AS NUMERIC)  < 80 THEN substr(ltrim(rtrim(DATE_STR)), 1, 2) ||'/' ||substr(ltrim(rtrim(DATE_STR)), 4, 2) || '/20' || substr(ltrim(rtrim(DATE_STR)), 7) ELSE substr(ltrim(rtrim(DATE_STR)), 1, 2) ||'/' ||substr(ltrim(rtrim(DATE_STR)), 4, 2)  || '/19' || substr(ltrim(rtrim(DATE_STR)), 7) END WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%d%m%Y') IS NOT NULL) AND length(ltrim(rtrim(DATE_STR))) = 8 THEN substr(ltrim(rtrim(DATE_STR)), 1, 2) ||'/' ||substr(ltrim(rtrim(DATE_STR)), 3, 2)  || '/' ||substr(ltrim(rtrim(DATE_STR)), 5) WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%y') IS NOT NULL) AND length(ltrim(rtrim(DATE_STR))) = 2 THEN CASE WHEN TRY_CAST(ltrim(rtrim(DATE_STR)) AS NUMERIC)    < 80 THEN '01/01/20' || ltrim(rtrim(DATE_STR)) ELSE '01/01/19' || ltrim(rtrim(DATE_STR)) END WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%m%Y') IS NOT NULL) AND (try_strptime(substr(ltrim(rtrim(DATE_STR)), 3), '%Y') IS NOT NULL) AND length(ltrim(rtrim(DATE_STR))) = 6 AND TRY_CAST(substr(ltrim(rtrim(DATE_STR)), 1, 2) AS NUMERIC)>0 AND TRY_CAST(substr(ltrim(rtrim(DATE_STR)), 1, 2) AS NUMERIC)<13 THEN '01/' ||substr(ltrim(rtrim(DATE_STR)), 1, 2)  || '/' ||substr(ltrim(rtrim(DATE_STR)), 3) WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%m%y') IS NOT NULL)  AND length(ltrim(rtrim(DATE_STR))) = 4 THEN CASE WHEN TRY_CAST(substr(ltrim(rtrim(DATE_STR)), 3) AS NUMERIC)    < 80 THEN '01/' || substr(ltrim(rtrim(DATE_STR)), 1, 2) || '/20' || substr(ltrim(rtrim(DATE_STR)), 3) ELSE '01/' || substr(ltrim(rtrim(DATE_STR)), 1, 2) || '/19' || substr(ltrim(rtrim(DATE_STR)), 3) END WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%Y') IS NOT NULL) AND length(ltrim(rtrim(DATE_STR))) = 4 THEN '01/01/' || ltrim(rtrim(DATE_STR)) WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%m/%y') IS NOT NULL)   AND  length(ltrim(rtrim(DATE_STR))) = 5 and substr(ltrim(rtrim(DATE_STR)), 3, 1) ='/' THEN CASE WHEN TRY_CAST(substr(ltrim(rtrim(DATE_STR)), 4) AS NUMERIC)   <80 THEN '01/' || substr(ltrim(rtrim(DATE_STR)), 1, 3) || '20' || substr(ltrim(rtrim(DATE_STR)), 4) ELSE '01/' || substr(ltrim(rtrim(DATE_STR)), 1, 3) || '19' || substr(ltrim(rtrim(DATE_STR)), 4) END WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%m/%y') IS NOT NULL)  AND length(ltrim(rtrim(DATE_STR))) = 5 and substr(ltrim(rtrim(DATE_STR)), 3, 1) ='\' THEN CASE WHEN TRY_CAST(substr(ltrim(rtrim(DATE_STR)), 4) AS NUMERIC)    < 80 THEN '01/' || substr(ltrim(rtrim(DATE_STR)), 1, 2) || '/20' || substr(ltrim(rtrim(DATE_STR)), 4) ELSE '01/' || substr(ltrim(rtrim(DATE_STR)), 1, 2) || '/19' || substr(ltrim(rtrim(DATE_STR)), 4) END WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%m/%y') IS NOT NULL) AND length(ltrim(rtrim(DATE_STR))) = 5 and substr(ltrim(rtrim(DATE_STR)), 3, 1) ='.' THEN CASE WHEN TRY_CAST(substr(ltrim(rtrim(DATE_STR)), 4) AS NUMERIC)    <80 THEN '01/' || substr(ltrim(rtrim(DATE_STR)), 1, 2) || '/20' || substr(ltrim(rtrim(DATE_STR)), 4) ELSE '01/' || substr(ltrim(rtrim(DATE_STR)), 1, 2) || '/19' || substr(ltrim(rtrim(DATE_STR)), 4) END WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%m/%Y') IS NOT NULL) AND length(ltrim(rtrim(DATE_STR))) = 7 AND substr(ltrim(rtrim(DATE_STR)), 3, 1) ='/' THEN '01/' || ltrim(rtrim(DATE_STR)) WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%m/%Y') IS NOT NULL) AND length(ltrim(rtrim(DATE_STR))) = 7  AND substr(ltrim(rtrim(DATE_STR)), 3, 1) ='\' THEN '01/' ||  substr(ltrim(rtrim(DATE_STR)), 1, 2)||'/'|| substr(ltrim(rtrim(DATE_STR)), 4) WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%m/%Y') IS NOT NULL) AND length(ltrim(rtrim(DATE_STR))) = 7  AND substr(ltrim(rtrim(DATE_STR)), 3, 1) ='.' THEN '01/' ||  substr(ltrim(rtrim(DATE_STR)), 1, 2)||'/'|| substr(ltrim(rtrim(DATE_STR)), 4) WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%d/%m/%y') IS NOT NULL)  AND length(ltrim(rtrim(DATE_STR))) = 8 AND substr(ltrim(rtrim(DATE_STR)), 3, 1) ='/' AND substr(ltrim(rtrim(DATE_STR)), 6, 1) ='/' THEN CASE WHEN TRY_CAST(substr(ltrim(rtrim(DATE_STR)), 7) AS NUMERIC)   < 80 THEN substr(ltrim(rtrim(DATE_STR)), 1, 6) || '20' || substr(ltrim(rtrim(DATE_STR)), 7) ELSE substr(ltrim(rtrim(DATE_STR)), 1, 6) || '19' || substr(ltrim(rtrim(DATE_STR)), 7) END WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%d/%m/%y') IS NOT NULL) AND length(ltrim(rtrim(DATE_STR))) = 8 AND substr(ltrim(rtrim(DATE_STR)), 3, 1) ='\' AND substr(ltrim(rtrim(DATE_STR)), 6, 1) ='\' THEN CASE WHEN TRY_CAST(substr(ltrim(rtrim(DATE_STR)), 7) AS NUMERIC)    < 80 THEN substr(ltrim(rtrim(DATE_STR)), 1, 2) ||'/' ||substr(ltrim(rtrim(DATE_STR)), 4, 2) || '/20' || substr(ltrim(rtrim(DATE_STR)), 7) ELSE substr(ltrim(rtrim(DATE_STR)), 1, 2) ||'/' ||substr(ltrim(rtrim(DATE_STR)), 4, 2)  || '/19' || substr(ltrim(rtrim(DATE_STR)), 7) END WHEN length(DATE_STR)=8 and  substr(DATE_STR, 3, 2)='//' and (TRY_CAST(substr(DATE_STR, 1, 2) AS NUMERIC) IS NOT NULL) AND TRY_CAST(substr(DATE_STR, 1, 2) AS INT) >= 1 AND TRY_CAST(substr(DATE_STR, 1, 2) AS INT) <= 12 and (TRY_CAST(substr(DATE_STR, 5, 4) AS NUMERIC) IS NOT NULL) AND TRY_CAST(substr(DATE_STR, 5, 4) AS INT) >= 1900 THEN '01/'||substr(SERVICE_START_RAW_in, 1, 2)||'/'|| substr(SERVICE_START_RAW_in, 5, 4) WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%d/%m/%Y') IS NOT NULL) AND length(ltrim(rtrim(DATE_STR))) = 10 AND substr(ltrim(rtrim(DATE_STR)), 3, 1) ='/' AND substr(ltrim(rtrim(DATE_STR)), 6, 1) ='/' THEN ltrim(rtrim(DATE_STR)) WHEN (try_strptime(ltrim(rtrim(DATE_STR)), '%d/%m/%Y') IS NOT NULL) AND length(ltrim(rtrim(DATE_STR))) = 10 AND substr(ltrim(rtrim(DATE_STR)), 3, 1) ='\' AND substr(ltrim(rtrim(DATE_STR)), 6, 1) ='\' THEN substr(ltrim(rtrim(DATE_STR)), 1, 2) ||'/' ||substr(ltrim(rtrim(DATE_STR)), 4, 2)  || '/' ||substr(ltrim(rtrim(DATE_STR)), 7) ELSE NULL END AS DATE_CHECK1,
        CASE WHEN length(ltrim(rtrim(DATE_STR))) = 7 AND substr(ltrim(rtrim(DATE_STR)), 3, 1) ='/' AND substr(ltrim(rtrim(DATE_STR)), 5, 1) ='/' THEN CASE WHEN TRY_CAST(substr(ltrim(rtrim(DATE_STR)), 6) AS NUMERIC)   < 26 THEN substr(ltrim(rtrim(DATE_STR)), 1, 3) ||'0'|| substr(ltrim(rtrim(DATE_STR)), 4, 2) || '20' ||substr(ltrim(rtrim(DATE_STR)), 6, 2) ELSE substr(ltrim(rtrim(DATE_STR)), 1, 3) ||'0'|| substr(ltrim(rtrim(DATE_STR)), 4, 2) || '19' || substr(ltrim(rtrim(DATE_STR)), 6) END ELSE null END AS DATE_CHECK11
    FROM int_exp_fields_prep base

),

    lkp_lkp_ref_dim_csr_agent_keys_start AS (
    SELECT *
    FROM (
        SELECT
            src.*,
        lkp.CSR_AGENT_KEY_PK AS CSR_AGENT_KEY_PK_START_with_objid,
        lkp.KEY_TYPE_CODE AS KEY_TYPE_CODE,
        lkp.STAFF_NUM AS CSR_NUM_START_with_objid,
        lkp.POSITION_CODE AS POSITION_CODE_START_with_objid,
        lkp.POSITION_FULL_DESC AS POSITION_FULL_DESC,
        lkp.POSITION_CLASS_CODE AS POSITION_CLASS_CODE,
        lkp.POSITION_CLASS_DESC AS POSITION_CLASS_DESC,
        lkp.EMP_ID AS EMP_ID,
        lkp.POSITION_FACILITY_CODE AS POSITION_FACILITY_CODE,
        lkp.POSITION_FACILITY_DESC AS POSITION_FACILITY_DESC,
        lkp.POSITION_AS400_ROLE_CODE AS POSITION_AS400_ROLE_CODE,
        lkp.POSITION_ROLE_CODE AS POSITION_ROLE_CODE,
        lkp.TERMINAL_ID AS TERMINAL_ID,
        lkp.AGREEMENT_TYPE_CODE AS AGREEMENT_TYPE_CODE,
        lkp.SUBSTITUTION_IND AS SUBSTITUTION_IND,
        lkp.POSITION_SUB_PAY_FACTOR_CODE AS POSITION_SUB_PAY_FACTOR_CODE,
        lkp.POSITION_SUB_PAY_FACTOR_DESC AS POSITION_SUB_PAY_FACTOR_DESC,
        lkp.EMP_NAME AS EMP_NAME,
        lkp.EMP_USER_NAME AS EMP_USER_NAME,
        lkp.ORG_UNIT_CODE AS ORG_UNIT_CODE,
        lkp.ORG_UNIT_FULL_DESC AS ORG_UNIT_FULL_DESC,
        lkp.NON_FICTIVE_ORG_UNIT_CODE AS NON_FICTIVE_ORG_UNIT_CODE,
        lkp.NON_FICTIVE_ORG_UNIT_DESC AS NON_FICTIVE_ORG_UNIT_DESC,
        lkp.ASSIGNED_ORG_UNIT_CODE AS ASSIGNED_ORG_UNIT_CODE,
        lkp.ASSIGNED_ORG_UNIT_DESC AS ASSIGNED_ORG_UNIT_DESC,
        lkp.ORG_UNIT_FACILITY_CODE AS ORG_UNIT_FACILITY_CODE,
        lkp.ORG_UNIT_FACILITY_DESC AS ORG_UNIT_FACILITY_DESC,
        lkp.ORG_UNIT_FACILITY_TYPE_CODE AS ORG_UNIT_FACILITY_TYPE_CODE,
        lkp.ORG_UNIT_FACILITY_TYPE_DESC AS ORG_UNIT_FACILITY_TYPE_DESC,
        lkp.ORG_UNIT_FACILITY_SUB_TYPE_CODE AS ORG_UNIT_FACILITY_SUB_TYPE_CODE,
        lkp.ORG_UNIT_FACILITY_SUB_TYPE_DESC AS ORG_UNIT_FACILITY_SUB_TYPE_DESC,
        lkp.FACILITY_OWNERSHIP_CODE AS FACILITY_OWNERSHIP_CODE,
        lkp.FACILITY_OWNERSHIP_DESC AS FACILITY_OWNERSHIP_DESC,
        lkp.BRANCH_CODE AS BRANCH_CODE,
        lkp.BRANCH_DESC AS BRANCH_DESC,
        lkp.AS400_BRANCH_CODE AS AS400_BRANCH_CODE,
        lkp.AS400_BRANCH_DESC AS AS400_BRANCH_DESC,
        lkp.REGION_CODE AS REGION_CODE,
        lkp.REGION_DESC AS REGION_DESC,
        lkp.DISTRICT_CODE AS DISTRICT_CODE,
        lkp.DISTRICT_DESC AS DISTRICT_DESC,
        lkp.BRANCH_CITY_CODE AS BRANCH_CITY_CODE,
        lkp.BRNAHC_CITY_DESC AS BRNAHC_CITY_DESC,
        lkp.OCCUPATION_CODE AS OCCUPATION_CODE,
        lkp.OCCUPATION_SHORT_DESC AS OCCUPATION_SHORT_DESC,
        lkp.OCCUPATION_FULL_DESC AS OCCUPATION_FULL_DESC,
        lkp.OCC_CLUSTER_CODE AS OCC_CLUSTER_CODE,
        lkp.OCC_CLUSTER_SHORT_DESC AS OCC_CLUSTER_SHORT_DESC,
        lkp.OCC_CLUSTER_FULL_DESC AS OCC_CLUSTER_FULL_DESC,
        lkp.OCC_FIELD_CODE AS OCC_FIELD_CODE,
        lkp.OCC_FIELD_SHORT_DESC AS OCC_FIELD_SHORT_DESC,
        lkp.OCC_FIELD_FULL_DESC AS OCC_FIELD_FULL_DESC,
        lkp.OCC_GROUP_CODE AS OCC_GROUP_CODE,
        lkp.OCC_GROUP_SHORT_DESC AS OCC_GROUP_SHORT_DESC,
        lkp.OCC_GROUP_FULL_DESC AS OCC_GROUP_FULL_DESC,
        lkp.EMP_GROUP_CODE AS EMP_GROUP_CODE,
        lkp.EMP_GROUP_DESC AS EMP_GROUP_DESC,
        lkp.EMP_SUB_GROUP_CODE AS EMP_SUB_GROUP_CODE,
        lkp.EMP_SUB_GROUP_DESC AS EMP_SUB_GROUP_DESC,
        lkp.BEGIN_DATE AS BEGIN_DATE,
        lkp.END_DATE AS END_DATE,
        lkp.IND_CURRENT AS IND_CURRENT,
        lkp.IS_DELETED AS IS_DELETED,
        lkp.LAST_RELEVANT_ROW_IND AS LAST_RELEVANT_ROW_IND,
        lkp.UPDATE_DATE AS UPDATE_DATE,
            ROW_NUMBER() OVER (PARTITION BY src.OBJID, src.CSR_AGENT_ID_int ORDER BY lkp.BEGIN_DATE DESC) AS rn
        FROM int_exp_fields src
        LEFT JOIN {{ source('dbo', 'ref_dim_csr_agent_keys') }} lkp
            ON TRY_CAST(lkp.OCCUPATION_CODE AS VARCHAR) = TRY_CAST(src.OBJID AS VARCHAR) AND TRY_CAST(lkp.EMP_ID AS VARCHAR) = TRY_CAST(src.CSR_AGENT_ID_int AS VARCHAR) AND TRY_CAST(lkp.BEGIN_DATE AS TIMESTAMP) <= TRY_CAST(src.SUBSCRIPTION_LOG_DATE AS TIMESTAMP) AND TRY_CAST(lkp.END_DATE AS TIMESTAMP) >= TRY_CAST(src.SUBSCRIPTION_LOG_DATE AS TIMESTAMP)
    ) deduped
    WHERE rn = 1

),

    lkp_lkp_ref_dim_csr_agent_keys_stop AS (
    SELECT *
    FROM (
        SELECT
            src.*,
        lkp.CSR_AGENT_KEY_PK AS CSR_AGENT_KEY_PK_STOP_with_objid,
        lkp.KEY_TYPE_CODE AS KEY_TYPE_CODE,
        lkp.STAFF_NUM AS CSR_NUM_STOP_with_objid,
        lkp.POSITION_CODE AS POSITION_CODE_STOP_with_objid,
        lkp.POSITION_FULL_DESC AS POSITION_FULL_DESC,
        lkp.POSITION_CLASS_CODE AS POSITION_CLASS_CODE,
        lkp.POSITION_CLASS_DESC AS POSITION_CLASS_DESC,
        lkp.EMP_ID AS EMP_ID,
        lkp.POSITION_FACILITY_CODE AS POSITION_FACILITY_CODE,
        lkp.POSITION_FACILITY_DESC AS POSITION_FACILITY_DESC,
        lkp.POSITION_AS400_ROLE_CODE AS POSITION_AS400_ROLE_CODE,
        lkp.POSITION_ROLE_CODE AS POSITION_ROLE_CODE,
        lkp.TERMINAL_ID AS TERMINAL_ID,
        lkp.AGREEMENT_TYPE_CODE AS AGREEMENT_TYPE_CODE,
        lkp.SUBSTITUTION_IND AS SUBSTITUTION_IND,
        lkp.POSITION_SUB_PAY_FACTOR_CODE AS POSITION_SUB_PAY_FACTOR_CODE,
        lkp.POSITION_SUB_PAY_FACTOR_DESC AS POSITION_SUB_PAY_FACTOR_DESC,
        lkp.EMP_NAME AS EMP_NAME,
        lkp.EMP_USER_NAME AS EMP_USER_NAME,
        lkp.ORG_UNIT_CODE AS ORG_UNIT_CODE,
        lkp.ORG_UNIT_FULL_DESC AS ORG_UNIT_FULL_DESC,
        lkp.NON_FICTIVE_ORG_UNIT_CODE AS NON_FICTIVE_ORG_UNIT_CODE,
        lkp.NON_FICTIVE_ORG_UNIT_DESC AS NON_FICTIVE_ORG_UNIT_DESC,
        lkp.ASSIGNED_ORG_UNIT_CODE AS ASSIGNED_ORG_UNIT_CODE,
        lkp.ASSIGNED_ORG_UNIT_DESC AS ASSIGNED_ORG_UNIT_DESC,
        lkp.ORG_UNIT_FACILITY_CODE AS ORG_UNIT_FACILITY_CODE,
        lkp.ORG_UNIT_FACILITY_DESC AS ORG_UNIT_FACILITY_DESC,
        lkp.ORG_UNIT_FACILITY_TYPE_CODE AS ORG_UNIT_FACILITY_TYPE_CODE,
        lkp.ORG_UNIT_FACILITY_TYPE_DESC AS ORG_UNIT_FACILITY_TYPE_DESC,
        lkp.ORG_UNIT_FACILITY_SUB_TYPE_CODE AS ORG_UNIT_FACILITY_SUB_TYPE_CODE,
        lkp.ORG_UNIT_FACILITY_SUB_TYPE_DESC AS ORG_UNIT_FACILITY_SUB_TYPE_DESC,
        lkp.FACILITY_OWNERSHIP_CODE AS FACILITY_OWNERSHIP_CODE,
        lkp.FACILITY_OWNERSHIP_DESC AS FACILITY_OWNERSHIP_DESC,
        lkp.BRANCH_CODE AS BRANCH_CODE,
        lkp.BRANCH_DESC AS BRANCH_DESC,
        lkp.AS400_BRANCH_CODE AS AS400_BRANCH_CODE,
        lkp.AS400_BRANCH_DESC AS AS400_BRANCH_DESC,
        lkp.REGION_CODE AS REGION_CODE,
        lkp.REGION_DESC AS REGION_DESC,
        lkp.DISTRICT_CODE AS DISTRICT_CODE,
        lkp.DISTRICT_DESC AS DISTRICT_DESC,
        lkp.BRANCH_CITY_CODE AS BRANCH_CITY_CODE,
        lkp.BRNAHC_CITY_DESC AS BRNAHC_CITY_DESC,
        lkp.OCCUPATION_CODE AS OCCUPATION_CODE,
        lkp.OCCUPATION_SHORT_DESC AS OCCUPATION_SHORT_DESC,
        lkp.OCCUPATION_FULL_DESC AS OCCUPATION_FULL_DESC,
        lkp.OCC_CLUSTER_CODE AS OCC_CLUSTER_CODE,
        lkp.OCC_CLUSTER_SHORT_DESC AS OCC_CLUSTER_SHORT_DESC,
        lkp.OCC_CLUSTER_FULL_DESC AS OCC_CLUSTER_FULL_DESC,
        lkp.OCC_FIELD_CODE AS OCC_FIELD_CODE,
        lkp.OCC_FIELD_SHORT_DESC AS OCC_FIELD_SHORT_DESC,
        lkp.OCC_FIELD_FULL_DESC AS OCC_FIELD_FULL_DESC,
        lkp.OCC_GROUP_CODE AS OCC_GROUP_CODE,
        lkp.OCC_GROUP_SHORT_DESC AS OCC_GROUP_SHORT_DESC,
        lkp.OCC_GROUP_FULL_DESC AS OCC_GROUP_FULL_DESC,
        lkp.EMP_GROUP_CODE AS EMP_GROUP_CODE,
        lkp.EMP_GROUP_DESC AS EMP_GROUP_DESC,
        lkp.EMP_SUB_GROUP_CODE AS EMP_SUB_GROUP_CODE,
        lkp.EMP_SUB_GROUP_DESC AS EMP_SUB_GROUP_DESC,
        lkp.BEGIN_DATE AS BEGIN_DATE,
        lkp.END_DATE AS END_DATE,
        lkp.IND_CURRENT AS IND_CURRENT,
        lkp.IS_DELETED AS IS_DELETED,
        lkp.LAST_RELEVANT_ROW_IND AS LAST_RELEVANT_ROW_IND,
        lkp.UPDATE_DATE AS UPDATE_DATE,
            ROW_NUMBER() OVER (PARTITION BY src.OBJID, src.CSR_AGENT_ID_int ORDER BY lkp.BEGIN_DATE DESC) AS rn
        FROM int_exp_fields src
        LEFT JOIN {{ source('dbo', 'ref_dim_csr_agent_keys') }} lkp
            ON TRY_CAST(lkp.OCCUPATION_CODE AS VARCHAR) = TRY_CAST(src.OBJID AS VARCHAR) AND TRY_CAST(lkp.EMP_ID AS VARCHAR) = TRY_CAST(src.CSR_AGENT_ID_int AS VARCHAR) AND TRY_CAST(lkp.BEGIN_DATE AS TIMESTAMP) <= TRY_CAST(src.SERVICE_END_DATE AS TIMESTAMP) AND TRY_CAST(lkp.END_DATE AS TIMESTAMP) >= TRY_CAST(src.SERVICE_END_DATE AS TIMESTAMP)
    ) deduped
    WHERE rn = 1

),

    lkp_lkp_ref_dim_csr_agent_keys_noobjid_start AS (
    SELECT *
    FROM (
        SELECT
            src.*,
        lkp.CSR_AGENT_KEY_PK AS CSR_AGENT_KEY_PK_START_no_objid,
        lkp.KEY_TYPE_CODE AS KEY_TYPE_CODE,
        lkp.STAFF_NUM AS CSR_NUM_START_no_objid,
        lkp.POSITION_CODE AS POSITION_CODE_START_no_objid,
        lkp.POSITION_FULL_DESC AS POSITION_FULL_DESC,
        lkp.POSITION_CLASS_CODE AS POSITION_CLASS_CODE,
        lkp.POSITION_CLASS_DESC AS POSITION_CLASS_DESC,
        lkp.EMP_ID AS EMP_ID,
        lkp.POSITION_FACILITY_CODE AS POSITION_FACILITY_CODE,
        lkp.POSITION_FACILITY_DESC AS POSITION_FACILITY_DESC,
        lkp.POSITION_AS400_ROLE_CODE AS POSITION_AS400_ROLE_CODE,
        lkp.POSITION_ROLE_CODE AS POSITION_ROLE_CODE,
        lkp.TERMINAL_ID AS TERMINAL_ID,
        lkp.AGREEMENT_TYPE_CODE AS AGREEMENT_TYPE_CODE,
        lkp.SUBSTITUTION_IND AS SUBSTITUTION_IND,
        lkp.POSITION_SUB_PAY_FACTOR_CODE AS POSITION_SUB_PAY_FACTOR_CODE,
        lkp.POSITION_SUB_PAY_FACTOR_DESC AS POSITION_SUB_PAY_FACTOR_DESC,
        lkp.EMP_NAME AS EMP_NAME,
        lkp.EMP_USER_NAME AS EMP_USER_NAME,
        lkp.ORG_UNIT_CODE AS ORG_UNIT_CODE,
        lkp.ORG_UNIT_FULL_DESC AS ORG_UNIT_FULL_DESC,
        lkp.NON_FICTIVE_ORG_UNIT_CODE AS NON_FICTIVE_ORG_UNIT_CODE,
        lkp.NON_FICTIVE_ORG_UNIT_DESC AS NON_FICTIVE_ORG_UNIT_DESC,
        lkp.ASSIGNED_ORG_UNIT_CODE AS ASSIGNED_ORG_UNIT_CODE,
        lkp.ASSIGNED_ORG_UNIT_DESC AS ASSIGNED_ORG_UNIT_DESC,
        lkp.ORG_UNIT_FACILITY_CODE AS ORG_UNIT_FACILITY_CODE,
        lkp.ORG_UNIT_FACILITY_DESC AS ORG_UNIT_FACILITY_DESC,
        lkp.ORG_UNIT_FACILITY_TYPE_CODE AS ORG_UNIT_FACILITY_TYPE_CODE,
        lkp.ORG_UNIT_FACILITY_TYPE_DESC AS ORG_UNIT_FACILITY_TYPE_DESC,
        lkp.ORG_UNIT_FACILITY_SUB_TYPE_CODE AS ORG_UNIT_FACILITY_SUB_TYPE_CODE,
        lkp.ORG_UNIT_FACILITY_SUB_TYPE_DESC AS ORG_UNIT_FACILITY_SUB_TYPE_DESC,
        lkp.FACILITY_OWNERSHIP_CODE AS FACILITY_OWNERSHIP_CODE,
        lkp.FACILITY_OWNERSHIP_DESC AS FACILITY_OWNERSHIP_DESC,
        lkp.BRANCH_CODE AS BRANCH_CODE,
        lkp.BRANCH_DESC AS BRANCH_DESC,
        lkp.AS400_BRANCH_CODE AS AS400_BRANCH_CODE,
        lkp.AS400_BRANCH_DESC AS AS400_BRANCH_DESC,
        lkp.REGION_CODE AS REGION_CODE,
        lkp.REGION_DESC AS REGION_DESC,
        lkp.DISTRICT_CODE AS DISTRICT_CODE,
        lkp.DISTRICT_DESC AS DISTRICT_DESC,
        lkp.BRANCH_CITY_CODE AS BRANCH_CITY_CODE,
        lkp.BRNAHC_CITY_DESC AS BRNAHC_CITY_DESC,
        lkp.OCCUPATION_CODE AS OCCUPATION_CODE,
        lkp.OCCUPATION_SHORT_DESC AS OCCUPATION_SHORT_DESC,
        lkp.OCCUPATION_FULL_DESC AS OCCUPATION_FULL_DESC,
        lkp.OCC_CLUSTER_CODE AS OCC_CLUSTER_CODE,
        lkp.OCC_CLUSTER_SHORT_DESC AS OCC_CLUSTER_SHORT_DESC,
        lkp.OCC_CLUSTER_FULL_DESC AS OCC_CLUSTER_FULL_DESC,
        lkp.OCC_FIELD_CODE AS OCC_FIELD_CODE,
        lkp.OCC_FIELD_SHORT_DESC AS OCC_FIELD_SHORT_DESC,
        lkp.OCC_FIELD_FULL_DESC AS OCC_FIELD_FULL_DESC,
        lkp.OCC_GROUP_CODE AS OCC_GROUP_CODE,
        lkp.OCC_GROUP_SHORT_DESC AS OCC_GROUP_SHORT_DESC,
        lkp.OCC_GROUP_FULL_DESC AS OCC_GROUP_FULL_DESC,
        lkp.EMP_GROUP_CODE AS EMP_GROUP_CODE,
        lkp.EMP_GROUP_DESC AS EMP_GROUP_DESC,
        lkp.EMP_SUB_GROUP_CODE AS EMP_SUB_GROUP_CODE,
        lkp.EMP_SUB_GROUP_DESC AS EMP_SUB_GROUP_DESC,
        lkp.BEGIN_DATE AS BEGIN_DATE,
        lkp.END_DATE AS END_DATE,
        lkp.IND_CURRENT AS IND_CURRENT,
        lkp.IS_DELETED AS IS_DELETED,
        lkp.LAST_RELEVANT_ROW_IND AS LAST_RELEVANT_ROW_IND,
        lkp.UPDATE_DATE AS UPDATE_DATE,
            ROW_NUMBER() OVER (PARTITION BY src.CSR_AGENT_ID_int ORDER BY lkp.BEGIN_DATE DESC) AS rn
        FROM int_exp_fields src
        LEFT JOIN {{ source('dbo', 'ref_dim_csr_agent_keys') }} lkp
            ON TRY_CAST(lkp.EMP_ID AS VARCHAR) = TRY_CAST(src.CSR_AGENT_ID_int AS VARCHAR) AND TRY_CAST(lkp.BEGIN_DATE AS TIMESTAMP) <= TRY_CAST(src.SUBSCRIPTION_LOG_DATE AS TIMESTAMP) AND TRY_CAST(lkp.END_DATE AS TIMESTAMP) >= TRY_CAST(src.SUBSCRIPTION_LOG_DATE AS TIMESTAMP)
    ) deduped
    WHERE rn = 1

),

    lkp_lkp_ref_dim_csr_agent_keys_noobjid_stop AS (
    SELECT *
    FROM (
        SELECT
            src.*,
        lkp.CSR_AGENT_KEY_PK AS CSR_AGENT_KEY_PK_STOP_no_objid,
        lkp.KEY_TYPE_CODE AS KEY_TYPE_CODE,
        lkp.STAFF_NUM AS CSR_NUM_STOP_no_objid,
        lkp.POSITION_CODE AS POSITION_CODE_STOP_no_objid,
        lkp.POSITION_FULL_DESC AS POSITION_FULL_DESC,
        lkp.POSITION_CLASS_CODE AS POSITION_CLASS_CODE,
        lkp.POSITION_CLASS_DESC AS POSITION_CLASS_DESC,
        lkp.EMP_ID AS EMP_ID,
        lkp.POSITION_FACILITY_CODE AS POSITION_FACILITY_CODE,
        lkp.POSITION_FACILITY_DESC AS POSITION_FACILITY_DESC,
        lkp.POSITION_AS400_ROLE_CODE AS POSITION_AS400_ROLE_CODE,
        lkp.POSITION_ROLE_CODE AS POSITION_ROLE_CODE,
        lkp.TERMINAL_ID AS TERMINAL_ID,
        lkp.AGREEMENT_TYPE_CODE AS AGREEMENT_TYPE_CODE,
        lkp.SUBSTITUTION_IND AS SUBSTITUTION_IND,
        lkp.POSITION_SUB_PAY_FACTOR_CODE AS POSITION_SUB_PAY_FACTOR_CODE,
        lkp.POSITION_SUB_PAY_FACTOR_DESC AS POSITION_SUB_PAY_FACTOR_DESC,
        lkp.EMP_NAME AS EMP_NAME,
        lkp.EMP_USER_NAME AS EMP_USER_NAME,
        lkp.ORG_UNIT_CODE AS ORG_UNIT_CODE,
        lkp.ORG_UNIT_FULL_DESC AS ORG_UNIT_FULL_DESC,
        lkp.NON_FICTIVE_ORG_UNIT_CODE AS NON_FICTIVE_ORG_UNIT_CODE,
        lkp.NON_FICTIVE_ORG_UNIT_DESC AS NON_FICTIVE_ORG_UNIT_DESC,
        lkp.ASSIGNED_ORG_UNIT_CODE AS ASSIGNED_ORG_UNIT_CODE,
        lkp.ASSIGNED_ORG_UNIT_DESC AS ASSIGNED_ORG_UNIT_DESC,
        lkp.ORG_UNIT_FACILITY_CODE AS ORG_UNIT_FACILITY_CODE,
        lkp.ORG_UNIT_FACILITY_DESC AS ORG_UNIT_FACILITY_DESC,
        lkp.ORG_UNIT_FACILITY_TYPE_CODE AS ORG_UNIT_FACILITY_TYPE_CODE,
        lkp.ORG_UNIT_FACILITY_TYPE_DESC AS ORG_UNIT_FACILITY_TYPE_DESC,
        lkp.ORG_UNIT_FACILITY_SUB_TYPE_CODE AS ORG_UNIT_FACILITY_SUB_TYPE_CODE,
        lkp.ORG_UNIT_FACILITY_SUB_TYPE_DESC AS ORG_UNIT_FACILITY_SUB_TYPE_DESC,
        lkp.FACILITY_OWNERSHIP_CODE AS FACILITY_OWNERSHIP_CODE,
        lkp.FACILITY_OWNERSHIP_DESC AS FACILITY_OWNERSHIP_DESC,
        lkp.BRANCH_CODE AS BRANCH_CODE,
        lkp.BRANCH_DESC AS BRANCH_DESC,
        lkp.AS400_BRANCH_CODE AS AS400_BRANCH_CODE,
        lkp.AS400_BRANCH_DESC AS AS400_BRANCH_DESC,
        lkp.REGION_CODE AS REGION_CODE,
        lkp.REGION_DESC AS REGION_DESC,
        lkp.DISTRICT_CODE AS DISTRICT_CODE,
        lkp.DISTRICT_DESC AS DISTRICT_DESC,
        lkp.BRANCH_CITY_CODE AS BRANCH_CITY_CODE,
        lkp.BRNAHC_CITY_DESC AS BRNAHC_CITY_DESC,
        lkp.OCCUPATION_CODE AS OCCUPATION_CODE,
        lkp.OCCUPATION_SHORT_DESC AS OCCUPATION_SHORT_DESC,
        lkp.OCCUPATION_FULL_DESC AS OCCUPATION_FULL_DESC,
        lkp.OCC_CLUSTER_CODE AS OCC_CLUSTER_CODE,
        lkp.OCC_CLUSTER_SHORT_DESC AS OCC_CLUSTER_SHORT_DESC,
        lkp.OCC_CLUSTER_FULL_DESC AS OCC_CLUSTER_FULL_DESC,
        lkp.OCC_FIELD_CODE AS OCC_FIELD_CODE,
        lkp.OCC_FIELD_SHORT_DESC AS OCC_FIELD_SHORT_DESC,
        lkp.OCC_FIELD_FULL_DESC AS OCC_FIELD_FULL_DESC,
        lkp.OCC_GROUP_CODE AS OCC_GROUP_CODE,
        lkp.OCC_GROUP_SHORT_DESC AS OCC_GROUP_SHORT_DESC,
        lkp.OCC_GROUP_FULL_DESC AS OCC_GROUP_FULL_DESC,
        lkp.EMP_GROUP_CODE AS EMP_GROUP_CODE,
        lkp.EMP_GROUP_DESC AS EMP_GROUP_DESC,
        lkp.EMP_SUB_GROUP_CODE AS EMP_SUB_GROUP_CODE,
        lkp.EMP_SUB_GROUP_DESC AS EMP_SUB_GROUP_DESC,
        lkp.BEGIN_DATE AS BEGIN_DATE,
        lkp.END_DATE AS END_DATE,
        lkp.IND_CURRENT AS IND_CURRENT,
        lkp.IS_DELETED AS IS_DELETED,
        lkp.LAST_RELEVANT_ROW_IND AS LAST_RELEVANT_ROW_IND,
        lkp.UPDATE_DATE AS UPDATE_DATE,
            ROW_NUMBER() OVER (PARTITION BY src.CSR_AGENT_ID_int ORDER BY lkp.BEGIN_DATE DESC) AS rn
        FROM int_exp_fields src
        LEFT JOIN {{ source('dbo', 'ref_dim_csr_agent_keys') }} lkp
            ON TRY_CAST(lkp.EMP_ID AS VARCHAR) = TRY_CAST(src.CSR_AGENT_ID_int AS VARCHAR) AND TRY_CAST(lkp.BEGIN_DATE AS TIMESTAMP) <= TRY_CAST(src.SERVICE_END_DATE AS TIMESTAMP) AND TRY_CAST(lkp.END_DATE AS TIMESTAMP) >= TRY_CAST(src.SERVICE_END_DATE AS TIMESTAMP)
    ) deduped
    WHERE rn = 1

),

    lkp_lkp_ref_dim_rate_plan AS (
    SELECT *
    FROM (
        SELECT
            src.*,
        lkp.RATE_PLAN_PK AS RATE_PLAN_PK,
        lkp.PRODUCT_FAMILY_CODE AS PRODUCT_FAMILY_CODE,
        lkp.PRODUCT_FAMILY_DESC AS PRODUCT_FAMILY_DESC,
        lkp.PRODUCT_GROUP_CODE AS PRODUCT_GROUP_CODE,
        lkp.PRODUCT_GROUP_DESC AS PRODUCT_GROUP_DESC,
        lkp.RATE_PLAN_CODE AS RATE_PLAN_CODE,
        lkp.RATE_PLAN_DESC AS RATE_PLAN_DESC,
        lkp.RATE_PLAN_CALC_DESC AS RATE_PLAN_CALC_DESC,
        lkp.RATE_PLAN_CODE_Y AS RATE_PLAN_CODE_Y,
        lkp.RATING_CATEGORY AS RATING_CATEGORY,
        lkp.RATE_PLAN_CODE_LOCAL_DESC AS RATE_PLAN_CODE_LOCAL_DESC,
        lkp.RATE_PLAN_CODE_ENG_DESC AS RATE_PLAN_CODE_ENG_DESC,
        lkp.LEVEL_NUM AS LEVEL_NUM,
        lkp.IND_CURRENT AS IND_CURRENT,
        lkp.START_DATE AS START_DATE,
        lkp.END_DATE AS END_DATE,
        lkp.CREATE_DATE AS CREATE_DATE,
        lkp.UPDATE_DATE AS UPDATE_DATE,
            ROW_NUMBER() OVER (PARTITION BY src.RATE_PLAN_CODE ORDER BY 1) AS rn
        FROM int_exp_fields src
        LEFT JOIN {{ source('dbo', 'ref_dim_rate_plan') }} lkp
            ON TRY_CAST(lkp.RATE_PLAN_CODE_Y AS VARCHAR) = TRY_CAST(src.RATE_PLAN_CODE AS VARCHAR)
    ) deduped
    WHERE rn = 1

),

    int_exp_bind AS (
    SELECT
        base.RECORD_CREATED_AT AS SUBSCRIPTION_CREATE_DATE,
        base.CSR_AGENT_ID AS CSR_AGENT_ID_STR,
        base.BILLING_ENTITY_CODE AS BILLING_ENTITY_CODE,
        base.BILLING_ENTITY_NAME AS BILLING_ENTITY_NAME,
        base.CSR_ROLE_CODE AS CSR_ROLE_CODE_src,
        base.CSR_NUMBER AS CSR_NUMBER_src,
        base.o_MARKET_SEGMENT_CODE AS MARKET_SEGMENT_CODE,
        base.CSR_AGENT_ID_int AS CSR_AGENT_ID,
        base.MARKET_SEGMENT_NAME AS MARKET_SEGMENT_NAME,
        base.CSR_AGENT_NAME AS CSR_AGENT_NAME,
        base.SOURCE_TABLE AS SOURCE_TABLE,
        base.ACTION AS ACTION,
        base.TRANSACTION_ID AS TRANSACTION_ID,
        base.MASTER_AUTO_EXPORT_BATCH_ID AS MASTER_AUTO_EXPORT_BATCH_ID,
        base.SERVICE_END_REASON AS SERVICE_END_REASON,
        base.SERVICE_END_DATE AS SERVICE_END_DATE,
        base.SUBSCRIPTION_LOG_DATE AS SUBSCRIPTION_LOG_DATE,
        base.SUBSCRIPTION_EVENT_NOTE AS SUBSCRIPTION_EVENT_NOTE,
        base.SERVICE_START_RAW_out AS SERVICE_BEGIN_DATE,
        base.RATING_ATTR2_CODE AS RATING_ATTR2_CODE,
        base.RATING_ATTR1_CODE AS RATING_ATTR1_CODE,
        base.RATE_PLAN_CODE AS RATE_PLAN_CODE,
        base.LINE_ITEM_NUM AS LINE_ITEM_NUM,
        base.ACCOUNT_CODE AS ACCOUNT_CODE,
        base.ACCOUNT_ID AS ACCOUNT_ID,
        base.SUBSCRIPTION_CREATE_DATE_trunc AS SUBSCRIPTION_CREATE_DATE_trunc,
        base.SUBSCRIPTION_SUBSCRIPTION_EVENT_KEY AS SUBSCRIPTION_SUBSCRIPTION_EVENT_KEY,
        base.CLOSED_BY AS CLOSED_BY,
        base.RATE_PLAN_PK AS RATE_PLAN_PK_DIM,
        base.RATE_PLAN AS RATE_PLAN,
        u0.POSITION_CODE_START_with_objid AS POSITION_CODE_START_with_objid,
        u0.CSR_NUM_START_with_objid AS CSR_NUM_START_with_objid,
        u0.CSR_AGENT_KEY_PK_START_with_objid AS CSR_AGENT_KEY_PK_START_with_objid,
        u0.CSR_AGENT_ID_int AS CSR_AGENT_ID_check,
        u1.CSR_AGENT_KEY_PK_STOP_with_objid AS CSR_AGENT_KEY_PK_STOP_with_objid,
        u1.POSITION_CODE_STOP_with_objid AS POSITION_CODE_STOP_with_objid,
        u1.CSR_NUM_STOP_with_objid AS CSR_NUM_STOP_with_objid,
        u2.CSR_NUM_START_no_objid AS CSR_NUM_START_no_objid,
        u2.CSR_AGENT_KEY_PK_START_no_objid AS CSR_AGENT_KEY_PK_START_no_objid,
        u2.POSITION_CODE_START_no_objid AS POSITION_CODE_START_no_objid,
        u3.POSITION_CODE_STOP_no_objid AS POSITION_CODE_STOP_no_objid,
        u3.CSR_NUM_STOP_no_objid AS CSR_NUM_STOP_no_objid,
        u3.CSR_AGENT_KEY_PK_STOP_no_objid AS CSR_AGENT_KEY_PK_STOP_no_objid,
        u4.RATE_PLAN_PK AS RATE_PLAN_PK,
        base.*
    FROM int_exp_fields base
    LEFT JOIN lkp_lkp_ref_dim_csr_agent_keys_start u0 ON base.OBJID = u0.OBJID AND base.CSR_AGENT_ID_int = u0.CSR_AGENT_ID_int
    LEFT JOIN lkp_lkp_ref_dim_csr_agent_keys_stop u1 ON base.OBJID = u1.OBJID AND base.CSR_AGENT_ID_int = u1.CSR_AGENT_ID_int
    LEFT JOIN lkp_lkp_ref_dim_csr_agent_keys_noobjid_start u2 ON base.CSR_AGENT_ID_int = u2.CSR_AGENT_ID_int
    LEFT JOIN lkp_lkp_ref_dim_csr_agent_keys_noobjid_stop u3 ON base.CSR_AGENT_ID_int = u3.CSR_AGENT_ID_int
    LEFT JOIN lkp_lkp_ref_dim_rate_plan u4 ON base.RATE_PLAN_CODE = u4.RATE_PLAN_CODE

),

    int_exp_prep AS (
    SELECT
        base.*,
        CASE WHEN (CSR_NUM_START_with_objid IS NOT NULL) THEN TRY_CAST(CSR_NUM_START_with_objid AS BIGINT) WHEN (CSR_NUM_START_no_objid IS NOT NULL) THEN TRY_CAST(CSR_NUM_START_no_objid AS BIGINT) ELSE -1 END AS CSR_NUM_START_out
    FROM int_exp_bind base

),

    int_exp AS (
    SELECT
        base.*,
        COALESCE(RATE_PLAN_PK_DIM, RATE_PLAN_PK) AS RATE_PLAN_PK_OUT,
        CASE WHEN (CSR_AGENT_KEY_PK_START_with_objid IS NOT NULL) THEN TRY_CAST(CSR_AGENT_KEY_PK_START_with_objid AS BIGINT) WHEN (CSR_AGENT_KEY_PK_START_no_objid IS NOT NULL) THEN TRY_CAST(CSR_AGENT_KEY_PK_START_no_objid AS BIGINT) ELSE -1 END AS CSR_AGENT_KEY_PK_START_out,
        CASE WHEN (CSR_AGENT_ID_check IS NULL) THEN -1 ELSE TRY_CAST(CSR_NUM_START_out AS BIGINT) END AS START_CSR_NUMBER,
        CASE WHEN (POSITION_CODE_START_with_objid IS NOT NULL) THEN TRY_CAST(POSITION_CODE_START_with_objid AS BIGINT) WHEN (POSITION_CODE_START_no_objid IS NOT NULL) THEN TRY_CAST(POSITION_CODE_START_no_objid AS BIGINT) ELSE -1 END AS POSITION_CODE_START_out,
        CASE WHEN (CSR_AGENT_KEY_PK_STOP_with_objid IS NOT NULL) THEN TRY_CAST(CSR_AGENT_KEY_PK_STOP_with_objid AS BIGINT) WHEN (CSR_AGENT_KEY_PK_STOP_no_objid IS NOT NULL) THEN TRY_CAST(CSR_AGENT_KEY_PK_STOP_no_objid AS BIGINT) ELSE -1 END AS CSR_AGENT_KEY_PK_STOP_out,
        CASE WHEN (CSR_NUM_STOP_with_objid IS NOT NULL) THEN TRY_CAST(CSR_NUM_STOP_with_objid AS BIGINT) WHEN (CSR_NUM_STOP_no_objid IS NOT NULL) THEN TRY_CAST(CSR_NUM_STOP_no_objid AS BIGINT) ELSE -1 END AS CSR_NUM_STOP_out,
        CASE WHEN (POSITION_CODE_STOP_with_objid IS NOT NULL) THEN TRY_CAST(POSITION_CODE_STOP_with_objid AS BIGINT) WHEN (POSITION_CODE_STOP_no_objid IS NOT NULL) THEN TRY_CAST(POSITION_CODE_STOP_no_objid AS BIGINT) ELSE -1 END AS POSITION_CODE_STOP_out
    FROM int_exp_prep base

),

    int_agg_subscription_subscription_subscription_event_key AS (
    SELECT
        SUBSCRIPTION_SUBSCRIPTION_EVENT_KEY
    FROM int_exp base
    GROUP BY SUBSCRIPTION_SUBSCRIPTION_EVENT_KEY

)

SELECT
    SUBSCRIPTION_SUBSCRIPTION_EVENT_KEY AS SUBSCRIPTION_SUBSCRIPTION_EVENT_KEY
FROM int_agg_subscription_subscription_subscription_event_key

