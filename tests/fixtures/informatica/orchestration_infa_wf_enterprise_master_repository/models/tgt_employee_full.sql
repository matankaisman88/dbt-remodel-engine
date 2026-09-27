-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_employee_full"
  )
}}
-- Target: TGT_EMPLOYEE_FULL
-- Informatica Load Order: 1
-- Source Instances: SRC_DEPARTMENT, SRC_EMPLOYEE, SRC_MANAGER
WITH
    sq_sq_department AS (
SELECT DEPT_ID, DEPT_NAME FROM {{ source('dbo', 'src_department') }}
),

    sq_sq_employee AS (
SELECT EMP_ID, DEPT_ID, MGR_ID FROM {{ source('dbo', 'src_employee') }}
),

    int_jnr_dept AS (
    SELECT
        d.EMP_ID,
        m.DEPT_ID,
        d.MGR_ID,
        m.DEPT_NAME
    FROM sq_sq_department m
    INNER JOIN sq_sq_employee d
        ON m.DEPT_ID = d.DEPT_ID

),

    sq_sq_manager AS (
SELECT MGR_ID, MGR_NAME FROM {{ source('dbo', 'src_manager') }}
),

    int_jnr_mgr AS (
    SELECT
        m.EMP_ID,
        m.DEPT_ID,
        m.MGR_ID,
        m.DEPT_NAME,
        d.MGR_NAME
    FROM int_jnr_dept m
    INNER JOIN sq_sq_manager d
        ON m.MGR_ID = d.MGR_ID

)

SELECT
    EMP_ID AS EMP_ID,
    DEPT_NAME AS DEPT_NAME,
    MGR_NAME AS MGR_NAME
FROM int_jnr_mgr

