-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "billing_landing";
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE TABLE IF NOT EXISTS billing_landing.src_detail(RECORD_ID INTEGER, AUTO_EXPORT_BATCH_ID INTEGER);
INSERT INTO "billing_landing"."src_detail" ("RECORD_ID", "AUTO_EXPORT_BATCH_ID") SELECT 101, 5660 WHERE NOT EXISTS (SELECT 1 FROM "billing_landing"."src_detail" WHERE "RECORD_ID" = 101);
INSERT INTO "billing_landing"."src_detail" ("RECORD_ID", "AUTO_EXPORT_BATCH_ID") SELECT 102, 4267 WHERE NOT EXISTS (SELECT 1 FROM "billing_landing"."src_detail" WHERE "RECORD_ID" = 102);
INSERT INTO "billing_landing"."src_detail" ("RECORD_ID", "AUTO_EXPORT_BATCH_ID") SELECT 103, 1037 WHERE NOT EXISTS (SELECT 1 FROM "billing_landing"."src_detail" WHERE "RECORD_ID" = 103);
INSERT INTO "billing_landing"."src_detail" ("RECORD_ID", "AUTO_EXPORT_BATCH_ID") SELECT 104, NULL WHERE NOT EXISTS (SELECT 1 FROM "billing_landing"."src_detail" WHERE "RECORD_ID" = 104);
CREATE TABLE IF NOT EXISTS billing_landing.src_subscription_master(RECORD_ID INTEGER, MASTER_AUTO_EXPORT_BATCH_ID INTEGER, AUTO_EXPORT_BATCH_ID INTEGER);
INSERT INTO "billing_landing"."src_subscription_master" ("RECORD_ID", "MASTER_AUTO_EXPORT_BATCH_ID", "AUTO_EXPORT_BATCH_ID") SELECT 101, 5660, 3534 WHERE NOT EXISTS (SELECT 1 FROM "billing_landing"."src_subscription_master" WHERE "RECORD_ID" = 101);
INSERT INTO "billing_landing"."src_subscription_master" ("RECORD_ID", "MASTER_AUTO_EXPORT_BATCH_ID", "AUTO_EXPORT_BATCH_ID") SELECT 102, 4267, 4584 WHERE NOT EXISTS (SELECT 1 FROM "billing_landing"."src_subscription_master" WHERE "RECORD_ID" = 102);
INSERT INTO "billing_landing"."src_subscription_master" ("RECORD_ID", "MASTER_AUTO_EXPORT_BATCH_ID", "AUTO_EXPORT_BATCH_ID") SELECT 103, 1037, 4329 WHERE NOT EXISTS (SELECT 1 FROM "billing_landing"."src_subscription_master" WHERE "RECORD_ID" = 103);
INSERT INTO "billing_landing"."src_subscription_master" ("RECORD_ID", "MASTER_AUTO_EXPORT_BATCH_ID", "AUTO_EXPORT_BATCH_ID") SELECT 104, NULL, NULL WHERE NOT EXISTS (SELECT 1 FROM "billing_landing"."src_subscription_master" WHERE "RECORD_ID" = 104);
CREATE TABLE IF NOT EXISTS dbo.tgt_out(RECORD_ID VARCHAR);
