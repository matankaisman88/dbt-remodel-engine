-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_claims_flagged"
  )
}}
-- Target: TGT_CLAIMS_FLAGGED
-- Informatica Load Order: 1
-- Source Instances: SRC_CLAIMS
WITH
    sq_sq_claims AS (
SELECT CLAIM_ID, STATUS, AMT, REGION FROM {{ source('dbo', 'src_claims') }}
),

    int_fil_active AS (
    SELECT
        base.*
    FROM sq_sq_claims base
    WHERE STATUS != 'VOID'

),

    int_rtr_high_low AS (
    SELECT
        *
    FROM int_fil_active base

),

    int_exp_high_flag AS (
    SELECT
        base.*,
        CLAIM_ID AS CLAIM_ID_O,
        STATUS AS STATUS_O,
        AMT AS AMT_O,
        REGION AS REGION_O,
        'HIGH' AS RISK_FLAG
    FROM int_rtr_high_low base

),

    int_exp_low_flag AS (
    SELECT
        base.*,
        CLAIM_ID AS CLAIM_ID_O,
        STATUS AS STATUS_O,
        AMT AS AMT_O,
        REGION AS REGION_O,
        'LOW' AS RISK_FLAG
    FROM int_rtr_high_low base

),

    int_un_flagged_claims AS (
    SELECT
        CLAIM_ID_O,
        STATUS_O,
        AMT_O,
        REGION_O,
        RISK_FLAG
    FROM int_exp_high_flag
    UNION ALL
    SELECT
        CLAIM_ID_O,
        STATUS_O,
        AMT_O,
        REGION_O,
        RISK_FLAG
    FROM int_exp_low_flag

)

SELECT
    CLAIM_ID_O AS CLAIM_ID_O,
    STATUS_O AS STATUS_O,
    AMT_O AS AMT_O,
    REGION_O AS REGION_O,
    RISK_FLAG AS RISK_FLAG
FROM int_un_flagged_claims

