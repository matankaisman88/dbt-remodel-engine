-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE TABLE IF NOT EXISTS dbo.src_customers(CUSTOMER_NAME VARCHAR);
INSERT INTO "dbo"."src_customers" ("CUSTOMER_NAME") VALUES ('customer_name_2');
INSERT INTO "dbo"."src_customers" ("CUSTOMER_NAME") VALUES ('customer_name_3');
INSERT INTO "dbo"."src_customers" ("CUSTOMER_NAME") VALUES ('customer_name_4');
INSERT INTO "dbo"."src_customers" ("CUSTOMER_NAME") VALUES (NULL);
CREATE TABLE IF NOT EXISTS dbo.tgt_customers(CUSTOMER_NAME VARCHAR);
