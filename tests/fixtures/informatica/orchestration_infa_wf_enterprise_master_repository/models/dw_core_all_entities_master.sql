-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "dw_core_all_entities_master"
  )
}}
-- Target: dw_core__all_entities_master
-- Informatica Load Order: 1
-- Source Instances: Fin_AP__Vendor_Master, HR_Core__Employee_Master, fin_ar__Customer_Master
WITH
    sq_sq_fin_ap_vendor_master AS (
SELECT * FROM {{ source('dbo', 'fin_ap__vendor_master') }}
),

    int_exp_tag_vendor AS (
    SELECT
        base.*,
        VENDOR_ID AS ENTITY_ID,
        VENDOR_NAME AS ENTITY_NAME,
        'VENDOR' AS ENTITY_TYPE
    FROM sq_sq_fin_ap_vendor_master base

),

    sq_sq_hr_core_employee_master AS (
SELECT * FROM {{ source('dbo', 'hr_core__employee_master') }}
),

    int_exp_tag_employee AS (
    SELECT
        base.*,
        EMP_ID AS ENTITY_ID,
        EMP_NAME AS ENTITY_NAME,
        'EMPLOYEE' AS ENTITY_TYPE
    FROM sq_sq_hr_core_employee_master base

),

    sq_sq_fin_ar_customer_master AS (
SELECT * FROM {{ source('dbo', 'fin_ar__customer_master') }}
),

    int_exp_tag_customer AS (
    SELECT
        base.*,
        CUST_ID AS ENTITY_ID,
        CUST_NAME AS ENTITY_NAME,
        'CUSTOMER' AS ENTITY_TYPE
    FROM sq_sq_fin_ar_customer_master base

),

    int_un_all_entities AS (
    SELECT
        ENTITY_ID,
        ENTITY_NAME,
        ENTITY_TYPE
    FROM int_exp_tag_vendor
    UNION ALL
    SELECT
        ENTITY_ID,
        ENTITY_NAME,
        ENTITY_TYPE
    FROM int_exp_tag_customer
    UNION ALL
    SELECT
        ENTITY_ID,
        ENTITY_NAME,
        ENTITY_TYPE
    FROM int_exp_tag_employee

)

SELECT
    ENTITY_ID AS ENTITY_ID,
    ENTITY_NAME AS ENTITY_NAME,
    ENTITY_TYPE AS ENTITY_TYPE
FROM int_un_all_entities

