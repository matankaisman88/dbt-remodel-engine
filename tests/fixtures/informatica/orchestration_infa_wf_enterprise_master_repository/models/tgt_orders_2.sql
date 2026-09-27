-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_orders"
  )
}}
-- Target: TGT_ORDERS
-- Informatica Load Order: 1
SELECT
    CAST(NULL AS INTEGER) /* unmapped in source mapping */ AS ORDER_ID,
    CAST(NULL AS INTEGER) /* unmapped in source mapping */ AS CUSTOMER_ID,
    CAST(NULL AS VARCHAR) /* unmapped in source mapping */ AS CREATED_DATE
FROM /* missing_upstream */

