-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE TABLE IF NOT EXISTS dbo.src_raw_labels(LABEL_TEXT VARCHAR);
INSERT INTO "dbo"."src_raw_labels" ("LABEL_TEXT") VALUES ('label_text_2');
INSERT INTO "dbo"."src_raw_labels" ("LABEL_TEXT") VALUES ('label_text_3');
INSERT INTO "dbo"."src_raw_labels" ("LABEL_TEXT") VALUES ('label_text_4');
INSERT INTO "dbo"."src_raw_labels" ("LABEL_TEXT") VALUES (NULL);
CREATE TABLE IF NOT EXISTS dbo.tgt_clean_labels(LABEL_TEXT VARCHAR);
