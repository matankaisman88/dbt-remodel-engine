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
SELECT
    CAST(NULL AS VARCHAR) /* unmapped in source mapping */ AS FULL_NAME
FROM /* missing_upstream */

