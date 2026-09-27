-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_accounts"
  )
}}
-- Target: TGT_ACCOUNTS
-- Informatica Load Order: 1
-- Source Instances: SRC_NEW_ACCOUNTS
WITH
    sq_sq_new_accounts AS (
SELECT ACCT_NAME FROM {{ source('dbo', 'src_new_accounts') }}
),

    int_exp_acct_key AS (
    SELECT
        base.*,
        ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS ACCT_ID,
        ACCT_NAME AS ACCT_NAME_O
    FROM sq_sq_new_accounts base

)

SELECT
    ACCT_ID AS ACCT_ID,
    ACCT_NAME_O AS ACCT_NAME_O
FROM int_exp_acct_key

