-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE TABLE IF NOT EXISTS dbo.src_sales(SALESPERSON VARCHAR, REGION VARCHAR, AMT DOUBLE);
INSERT INTO "dbo"."src_sales" ("SALESPERSON", "REGION", "AMT") VALUES ('salesperson_2', 'region_2', 12.35);
INSERT INTO "dbo"."src_sales" ("SALESPERSON", "REGION", "AMT") VALUES ('salesperson_3', 'region_3', 12.36);
INSERT INTO "dbo"."src_sales" ("SALESPERSON", "REGION", "AMT") VALUES ('salesperson_4', 'region_4', 12.37);
INSERT INTO "dbo"."src_sales" ("SALESPERSON", "REGION", "AMT") VALUES (NULL, NULL, NULL);
CREATE TABLE IF NOT EXISTS dbo.tgt_region_summary(REGION VARCHAR, TOTAL_AMT VARCHAR, SALES_COUNT VARCHAR);
