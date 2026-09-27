-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_row"
  )
}}
-- Target: TGT_ROW
-- Informatica Load Order: 1
-- Source Instances: SRC_ROW
WITH
    sq_sq_row AS (
SELECT ID FROM {{ source('dbo', 'src_row') }}
)

SELECT
    ID AS ID
FROM sq_sq_row

