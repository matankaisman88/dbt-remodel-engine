-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_contacts"
  )
}}
-- Target: TGT_CONTACTS
-- Informatica Load Order: 2
-- Source Instances: SRC_NEW_CONTACTS
WITH
    sq_sq_new_contacts AS (
SELECT CONTACT_NAME FROM {{ source('dbo', 'src_new_contacts') }}
),

    int_exp_contact_key AS (
    SELECT
        base.*,
        ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS CONTACT_ID,
        CONTACT_NAME AS CONTACT_NAME_O
    FROM sq_sq_new_contacts base

)

SELECT
    CONTACT_ID AS CONTACT_ID,
    CONTACT_NAME_O AS CONTACT_NAME_O
FROM int_exp_contact_key

