-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE TABLE IF NOT EXISTS dbo.src_customer_changes(CUST_ID INTEGER, CUST_NAME VARCHAR, CHANGE_TYPE VARCHAR);
INSERT INTO "dbo"."src_customer_changes" ("CUST_ID", "CUST_NAME", "CHANGE_TYPE") SELECT 755, 'cust_name_3', 'PENDING' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_customer_changes" WHERE "CUST_ID" = 755);
INSERT INTO "dbo"."src_customer_changes" ("CUST_ID", "CUST_NAME", "CHANGE_TYPE") SELECT 1170, 'cust_name_2', 'COMPLETED' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_customer_changes" WHERE "CUST_ID" = 1170);
INSERT INTO "dbo"."src_customer_changes" ("CUST_ID", "CUST_NAME", "CHANGE_TYPE") SELECT 6296, 'cust_name_4', 'CANCELLED' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_customer_changes" WHERE "CUST_ID" = 6296);
INSERT INTO "dbo"."src_customer_changes" ("CUST_ID", "CUST_NAME", "CHANGE_TYPE") VALUES (NULL, NULL, NULL);
CREATE TABLE IF NOT EXISTS dbo.tgt_customer_scd(SURROGATE_KEY VARCHAR, CUST_ID_O VARCHAR, CUST_NAME_O VARCHAR);
