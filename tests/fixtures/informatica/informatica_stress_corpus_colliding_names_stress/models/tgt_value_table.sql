-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_value_table"
  )
}}
-- Target: TGT_VALUE_TABLE
-- Informatica Load Order: 1
-- Source Instances: VALUE
WITH
    sq_sq_value AS (
SELECT VALUE, ID FROM {{ source('dbo', 'value') }}
),

    int_value_exp AS (
    SELECT
        base.*
    FROM sq_sq_value base

)

SELECT
    VALUE AS VALUE,
    ID AS ID
FROM int_value_exp

