-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE TABLE IF NOT EXISTS dbo.dw_core__all_entities_master(ENTITY_ID VARCHAR, ENTITY_NAME VARCHAR, ENTITY_TYPE VARCHAR);
CREATE TABLE IF NOT EXISTS dbo.fin_ap__vendor_master(VENDOR_ID INTEGER, VENDOR_NAME VARCHAR);
INSERT INTO "dbo"."fin_ap__vendor_master" ("VENDOR_ID", "VENDOR_NAME") SELECT 754, 'vendor_name_3' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."fin_ap__vendor_master" WHERE "VENDOR_ID" = 754);
INSERT INTO "dbo"."fin_ap__vendor_master" ("VENDOR_ID", "VENDOR_NAME") SELECT 1169, 'vendor_name_2' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."fin_ap__vendor_master" WHERE "VENDOR_ID" = 1169);
INSERT INTO "dbo"."fin_ap__vendor_master" ("VENDOR_ID", "VENDOR_NAME") SELECT 6295, 'vendor_name_4' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."fin_ap__vendor_master" WHERE "VENDOR_ID" = 6295);
INSERT INTO "dbo"."fin_ap__vendor_master" ("VENDOR_ID", "VENDOR_NAME") VALUES (NULL, NULL);
CREATE TABLE IF NOT EXISTS dbo.fin_ar__customer_master(CUST_ID INTEGER, CUST_NAME VARCHAR);
INSERT INTO "dbo"."fin_ar__customer_master" ("CUST_ID", "CUST_NAME") SELECT 755, 'cust_name_3' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."fin_ar__customer_master" WHERE "CUST_ID" = 755);
INSERT INTO "dbo"."fin_ar__customer_master" ("CUST_ID", "CUST_NAME") SELECT 1170, 'cust_name_2' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."fin_ar__customer_master" WHERE "CUST_ID" = 1170);
INSERT INTO "dbo"."fin_ar__customer_master" ("CUST_ID", "CUST_NAME") SELECT 6296, 'cust_name_4' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."fin_ar__customer_master" WHERE "CUST_ID" = 6296);
INSERT INTO "dbo"."fin_ar__customer_master" ("CUST_ID", "CUST_NAME") VALUES (NULL, NULL);
CREATE TABLE IF NOT EXISTS dbo.hr_core__employee_master(EMP_ID INTEGER, EMP_NAME VARCHAR);
INSERT INTO "dbo"."hr_core__employee_master" ("EMP_ID", "EMP_NAME") SELECT 754, 'emp_name_3' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."hr_core__employee_master" WHERE "EMP_ID" = 754);
INSERT INTO "dbo"."hr_core__employee_master" ("EMP_ID", "EMP_NAME") SELECT 1169, 'emp_name_2' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."hr_core__employee_master" WHERE "EMP_ID" = 1169);
INSERT INTO "dbo"."hr_core__employee_master" ("EMP_ID", "EMP_NAME") SELECT 6295, 'emp_name_4' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."hr_core__employee_master" WHERE "EMP_ID" = 6295);
INSERT INTO "dbo"."hr_core__employee_master" ("EMP_ID", "EMP_NAME") VALUES (NULL, NULL);
