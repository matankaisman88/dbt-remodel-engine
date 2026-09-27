-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE TABLE IF NOT EXISTS dbo.src_row(ID INTEGER);
INSERT INTO "dbo"."src_row" ("ID") SELECT 755 WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_row" WHERE "ID" = 755);
INSERT INTO "dbo"."src_row" ("ID") SELECT 1170 WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_row" WHERE "ID" = 1170);
INSERT INTO "dbo"."src_row" ("ID") SELECT 6296 WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_row" WHERE "ID" = 6296);
INSERT INTO "dbo"."src_row" ("ID") VALUES (NULL);
CREATE TABLE IF NOT EXISTS dbo.tgt_row(ID INTEGER);
