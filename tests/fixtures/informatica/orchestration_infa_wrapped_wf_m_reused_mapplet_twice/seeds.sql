-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE TABLE IF NOT EXISTS dbo.src_product_names(PRODUCT_NAME VARCHAR);
INSERT INTO "dbo"."src_product_names" ("PRODUCT_NAME") VALUES ('product_name_2');
INSERT INTO "dbo"."src_product_names" ("PRODUCT_NAME") VALUES ('product_name_3');
INSERT INTO "dbo"."src_product_names" ("PRODUCT_NAME") VALUES ('product_name_4');
INSERT INTO "dbo"."src_product_names" ("PRODUCT_NAME") VALUES (NULL);
CREATE TABLE IF NOT EXISTS dbo.src_supplier_names(SUPPLIER_NAME VARCHAR);
INSERT INTO "dbo"."src_supplier_names" ("SUPPLIER_NAME") VALUES ('supplier_name_2');
INSERT INTO "dbo"."src_supplier_names" ("SUPPLIER_NAME") VALUES ('supplier_name_3');
INSERT INTO "dbo"."src_supplier_names" ("SUPPLIER_NAME") VALUES ('supplier_name_4');
INSERT INTO "dbo"."src_supplier_names" ("SUPPLIER_NAME") VALUES (NULL);
CREATE TABLE IF NOT EXISTS dbo.tgt_product_names_clean(PRODUCT_NAME VARCHAR);
CREATE TABLE IF NOT EXISTS dbo.tgt_supplier_names_clean(SUPPLIER_NAME VARCHAR);
