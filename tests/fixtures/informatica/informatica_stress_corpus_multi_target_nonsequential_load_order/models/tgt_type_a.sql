-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_type_a"
  )
}}
-- Target: TGT_TYPE_A
-- Informatica Load Order: 2
-- Source Instances: SRC_MASTER_DATA
WITH
    sq_sq_master_data AS (
SELECT ENTITY_ID, ENTITY_TYPE, VALUE FROM {{ source('dbo', 'src_master_data') }}
),

    int_rtr_type AS (
    SELECT
        *
    FROM sq_sq_master_data base

)

SELECT
    ENTITY_ID AS ENTITY_ID,
    ENTITY_TYPE AS ENTITY_TYPE,
    VALUE AS VALUE
FROM int_rtr_type

