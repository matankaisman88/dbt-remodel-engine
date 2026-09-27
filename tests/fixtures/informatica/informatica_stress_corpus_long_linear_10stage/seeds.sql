-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE TABLE IF NOT EXISTS dbo.ref_severity(LOG_ID_1 DOUBLE, MSG_1 VARCHAR, SEVERITY_1 VARCHAR, TS_1 VARCHAR, SEVERITY_CODE VARCHAR);
INSERT INTO "dbo"."ref_severity" ("LOG_ID_1", "MSG_1", "SEVERITY_1", "TS_1", "SEVERITY_CODE") VALUES (12.3400001, 'msg_1_2', 'severity_1_2', '2021-02-02', 'severity_code_2');
INSERT INTO "dbo"."ref_severity" ("LOG_ID_1", "MSG_1", "SEVERITY_1", "TS_1", "SEVERITY_CODE") VALUES (12.3400001, 'msg_1_3', 'severity_1_3', '2022-03-03', 'severity_code_3');
INSERT INTO "dbo"."ref_severity" ("LOG_ID_1", "MSG_1", "SEVERITY_1", "TS_1", "SEVERITY_CODE") VALUES (12.3400006, 'msg_1_4', 'severity_1_4', '2023-04-04', 'severity_code_4');
INSERT INTO "dbo"."ref_severity" ("LOG_ID_1", "MSG_1", "SEVERITY_1", "TS_1", "SEVERITY_CODE") VALUES (NULL, NULL, NULL, NULL, NULL);
CREATE TABLE IF NOT EXISTS dbo.src_raw_log(LOG_ID INTEGER, RAW_MSG VARCHAR, SEVERITY VARCHAR, TS VARCHAR);
INSERT INTO "dbo"."src_raw_log" ("LOG_ID", "RAW_MSG", "SEVERITY", "TS") SELECT 754, 'raw_msg_3', 'severity_3', '2022-03-03' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_raw_log" WHERE "LOG_ID" = 754);
INSERT INTO "dbo"."src_raw_log" ("LOG_ID", "RAW_MSG", "SEVERITY", "TS") SELECT 1169, 'raw_msg_2', 'severity_2', '2021-02-02' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_raw_log" WHERE "LOG_ID" = 1169);
INSERT INTO "dbo"."src_raw_log" ("LOG_ID", "RAW_MSG", "SEVERITY", "TS") SELECT 6295, 'raw_msg_4', 'severity_4', '2023-04-04' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_raw_log" WHERE "LOG_ID" = 6295);
INSERT INTO "dbo"."src_raw_log" ("LOG_ID", "RAW_MSG", "SEVERITY", "TS") VALUES (NULL, NULL, NULL, NULL);
CREATE TABLE IF NOT EXISTS dbo.tgt_log_processed(LOG_ID_1_2_c VARCHAR, MSG_1_2_c VARCHAR, SEVERITY_1_2_c VARCHAR, TS_1_2_c VARCHAR, SEVERITY_CODE_2_c VARCHAR, IS_CRIT VARCHAR);
