-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_inventory_valued"
  )
}}
-- Target: TGT_INVENTORY_VALUED
-- Informatica Load Order: 1
-- Source Instances: SRC_INVENTORY_MOVEMENT
WITH
    sq_sq_inventory_movement AS (
SELECT WAREHOUSE_ID, SKU, MOVE_DATE, QTY FROM {{ source('dbo', 'src_inventory_movement') }}
),

    lkp_lkp_unit_cost AS (
    SELECT
        src.*,
        lkp.UNIT_COST AS UNIT_COST,
        lkp.SUPPLIER_ID AS SUPPLIER_ID
    FROM sq_sq_inventory_movement src
    LEFT JOIN {{ source('dbo', 'ref_inventory_cost') }} lkp
        ON TRY_CAST(lkp.WAREHOUSE_ID AS VARCHAR) = TRY_CAST(src.WAREHOUSE_ID AS VARCHAR) AND lkp.SKU = src.SKU AND lkp.MOVE_DATE = src.MOVE_DATE

)

SELECT
    WAREHOUSE_ID AS WAREHOUSE_ID,
    SKU AS SKU,
    MOVE_DATE AS MOVE_DATE,
    QTY AS QTY,
    UNIT_COST AS UNIT_COST,
    SUPPLIER_ID AS SUPPLIER_ID
FROM lkp_lkp_unit_cost

