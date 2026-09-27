-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE TABLE IF NOT EXISTS dbo.src_department(DEPT_ID INTEGER, DEPT_NAME VARCHAR);
INSERT INTO "dbo"."src_department" ("DEPT_ID", "DEPT_NAME") SELECT 754, 'dept_name_3' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_department" WHERE "DEPT_ID" = 754);
INSERT INTO "dbo"."src_department" ("DEPT_ID", "DEPT_NAME") SELECT 1169, 'dept_name_2' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_department" WHERE "DEPT_ID" = 1169);
INSERT INTO "dbo"."src_department" ("DEPT_ID", "DEPT_NAME") SELECT 6295, 'dept_name_4' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_department" WHERE "DEPT_ID" = 6295);
INSERT INTO "dbo"."src_department" ("DEPT_ID", "DEPT_NAME") VALUES (NULL, NULL);
CREATE TABLE IF NOT EXISTS dbo.src_employee(EMP_ID INTEGER, DEPT_ID INTEGER, MGR_ID INTEGER);
INSERT INTO "dbo"."src_employee" ("EMP_ID", "DEPT_ID", "MGR_ID") SELECT 754, 5660, 3534 WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_employee" WHERE "EMP_ID" = 754);
INSERT INTO "dbo"."src_employee" ("EMP_ID", "DEPT_ID", "MGR_ID") SELECT 1169, 4267, 4584 WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_employee" WHERE "EMP_ID" = 1169);
INSERT INTO "dbo"."src_employee" ("EMP_ID", "DEPT_ID", "MGR_ID") SELECT 6295, 1037, 4329 WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_employee" WHERE "EMP_ID" = 6295);
INSERT INTO "dbo"."src_employee" ("EMP_ID", "DEPT_ID", "MGR_ID") VALUES (NULL, NULL, NULL);
CREATE TABLE IF NOT EXISTS dbo.src_manager(MGR_ID INTEGER, MGR_NAME VARCHAR);
INSERT INTO "dbo"."src_manager" ("MGR_ID", "MGR_NAME") SELECT 754, 'mgr_name_3' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_manager" WHERE "MGR_ID" = 754);
INSERT INTO "dbo"."src_manager" ("MGR_ID", "MGR_NAME") SELECT 1169, 'mgr_name_2' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_manager" WHERE "MGR_ID" = 1169);
INSERT INTO "dbo"."src_manager" ("MGR_ID", "MGR_NAME") SELECT 6295, 'mgr_name_4' WHERE NOT EXISTS (SELECT 1 FROM "dbo"."src_manager" WHERE "MGR_ID" = 6295);
INSERT INTO "dbo"."src_manager" ("MGR_ID", "MGR_NAME") VALUES (NULL, NULL);
CREATE TABLE IF NOT EXISTS dbo.tgt_employee_full(EMP_ID VARCHAR, DEPT_NAME VARCHAR, MGR_NAME VARCHAR);
