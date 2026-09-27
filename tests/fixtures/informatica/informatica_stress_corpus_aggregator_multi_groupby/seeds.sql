-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE TABLE IF NOT EXISTS dbo.src_sales_detail("YEAR" DOUBLE, "QUARTER" VARCHAR, REGION VARCHAR, PRODUCT_LINE VARCHAR, AMT DOUBLE);
INSERT INTO "dbo"."src_sales_detail" ("YEAR", "QUARTER", "REGION", "PRODUCT_LINE", "AMT") VALUES (12.3400001, 'quarter_2', 'region_2', 'product_line_2', 12.35);
INSERT INTO "dbo"."src_sales_detail" ("YEAR", "QUARTER", "REGION", "PRODUCT_LINE", "AMT") VALUES (12.3400001, 'quarter_3', 'region_3', 'product_line_3', 12.36);
INSERT INTO "dbo"."src_sales_detail" ("YEAR", "QUARTER", "REGION", "PRODUCT_LINE", "AMT") VALUES (12.3400006, 'quarter_4', 'region_4', 'product_line_4', 12.37);
INSERT INTO "dbo"."src_sales_detail" ("YEAR", "QUARTER", "REGION", "PRODUCT_LINE", "AMT") VALUES (NULL, NULL, NULL, NULL, NULL);
CREATE TABLE IF NOT EXISTS dbo.tgt_sales_rollup("YEAR" VARCHAR, "QUARTER" VARCHAR, REGION VARCHAR, PRODUCT_LINE VARCHAR, TOTAL_AMT VARCHAR, AVG_AMT VARCHAR, MAX_AMT VARCHAR);
