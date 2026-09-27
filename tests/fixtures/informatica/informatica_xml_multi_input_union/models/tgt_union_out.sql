-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_union_out"
  )
}}
-- Target: TGT_UNION_OUT
-- Informatica Load Order: 1
WITH
    sq_sq_branch_a AS (
SELECT 1 AS ENTITY_ID, 'A' AS CODE
),

    int_exp_branch_a AS (
    SELECT
        base.*
    FROM sq_sq_branch_a base

),

    sq_sq_branch_b AS (
SELECT 2 AS ENTITY_ID, 'B' AS CODE
),

    int_exp_branch_b AS (
    SELECT
        base.*
    FROM sq_sq_branch_b base

),

    sq_sq_branch_c AS (
SELECT 3 AS ENTITY_ID, 'C' AS CODE
),

    int_exp_branch_c AS (
    SELECT
        base.*
    FROM sq_sq_branch_c base

),

    int_union_custom AS (
    SELECT
        ENTITY_ID AS ENTITY_ID,
        CODE AS CODE
    FROM int_exp_branch_a
    UNION ALL
    SELECT
        ENTITY_ID AS ENTITY_ID,
        CODE AS CODE
    FROM int_exp_branch_b
    UNION ALL
    SELECT
        ENTITY_ID AS ENTITY_ID,
        CODE AS CODE
    FROM int_exp_branch_c

)

SELECT
    ENTITY_ID AS ENTITY_ID,
    CODE AS CODE
FROM int_union_custom

