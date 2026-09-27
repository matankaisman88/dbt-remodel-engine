-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_product_names_clean"
  )
}}
-- Target: TGT_PRODUCT_NAMES_CLEAN
-- Informatica Load Order: 1
SELECT
    CAST(NULL AS VARCHAR) /* unmapped in source mapping */ AS PRODUCT_NAME
FROM /* missing_upstream */

