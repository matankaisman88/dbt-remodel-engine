-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE TABLE IF NOT EXISTS dbo.src_raw_names(FULL_NAME VARCHAR);
INSERT INTO "dbo"."src_raw_names" ("FULL_NAME") VALUES ('full_name_2');
INSERT INTO "dbo"."src_raw_names" ("FULL_NAME") VALUES ('full_name_3');
INSERT INTO "dbo"."src_raw_names" ("FULL_NAME") VALUES ('full_name_4');
INSERT INTO "dbo"."src_raw_names" ("FULL_NAME") VALUES (NULL);
CREATE TABLE IF NOT EXISTS dbo.tgt_clean_names(FULL_NAME VARCHAR);
