-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_supplier_names_clean"
  )
}}
-- Target: TGT_SUPPLIER_NAMES_CLEAN
-- Informatica Load Order: 2
SELECT
    CAST(NULL AS VARCHAR) /* unmapped in source mapping */ AS SUPPLIER_NAME
FROM /* missing_upstream */

