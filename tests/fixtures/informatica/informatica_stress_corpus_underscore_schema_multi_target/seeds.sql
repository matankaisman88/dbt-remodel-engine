-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE SCHEMA IF NOT EXISTS "legacy_ops_tmp";
CREATE TABLE IF NOT EXISTS dbo.dw_core_tmp_staging_events_clean(EVENT_KEY VARCHAR, PAYLOAD VARCHAR, STATUS VARCHAR);
CREATE TABLE IF NOT EXISTS dbo.dw_core_tmp_staging_events_rejected(EVENT_KEY VARCHAR, PAYLOAD VARCHAR, STATUS VARCHAR);
CREATE TABLE IF NOT EXISTS dbo.legacy_ops_tmp_staging_raw_events(EVENT_KEY VARCHAR, PAYLOAD VARCHAR, STATUS VARCHAR);
INSERT INTO "dbo"."legacy_ops_tmp_staging_raw_events" ("EVENT_KEY", "PAYLOAD", "STATUS") SELECT '2021-02-02', 'payload_2', 'ACTIVE' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."legacy_ops_tmp_staging_raw_events" WHERE "EVENT_KEY" = '2021-02-02');
INSERT INTO "dbo"."legacy_ops_tmp_staging_raw_events" ("EVENT_KEY", "PAYLOAD", "STATUS") SELECT '2022-03-03', 'payload_3', 'ACTIVE' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."legacy_ops_tmp_staging_raw_events" WHERE "EVENT_KEY" = '2022-03-03');
INSERT INTO "dbo"."legacy_ops_tmp_staging_raw_events" ("EVENT_KEY", "PAYLOAD", "STATUS") SELECT '2023-04-04', 'payload_4', 'ACTIVE' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."legacy_ops_tmp_staging_raw_events" WHERE "EVENT_KEY" = '2023-04-04');
INSERT INTO "dbo"."legacy_ops_tmp_staging_raw_events" ("EVENT_KEY", "PAYLOAD", "STATUS") VALUES (NULL, NULL, 'ACTIVE');
CREATE TABLE IF NOT EXISTS legacy_ops_tmp.staging_raw_events(EVENT_KEY VARCHAR, PAYLOAD VARCHAR, STATUS VARCHAR);
INSERT INTO "legacy_ops_tmp"."staging_raw_events" ("EVENT_KEY", "PAYLOAD", "STATUS") SELECT '2021-02-02', 'payload_2', 'ACTIVE' WHERE NOT EXISTS (SELECT 1 FROM "legacy_ops_tmp"."staging_raw_events" WHERE "EVENT_KEY" = '2021-02-02');
INSERT INTO "legacy_ops_tmp"."staging_raw_events" ("EVENT_KEY", "PAYLOAD", "STATUS") SELECT '2022-03-03', 'payload_3', 'ACTIVE' WHERE NOT EXISTS (SELECT 1 FROM "legacy_ops_tmp"."staging_raw_events" WHERE "EVENT_KEY" = '2022-03-03');
INSERT INTO "legacy_ops_tmp"."staging_raw_events" ("EVENT_KEY", "PAYLOAD", "STATUS") SELECT '2023-04-04', 'payload_4', 'ACTIVE' WHERE NOT EXISTS (SELECT 1 FROM "legacy_ops_tmp"."staging_raw_events" WHERE "EVENT_KEY" = '2023-04-04');
INSERT INTO "legacy_ops_tmp"."staging_raw_events" ("EVENT_KEY", "PAYLOAD", "STATUS") VALUES (NULL, NULL, 'ACTIVE');
