-- Auto-generated DuckDB seed for Airflow dbt runs.
CREATE SCHEMA IF NOT EXISTS "dbo";
CREATE TABLE IF NOT EXISTS dbo.src_new_accounts(ACCT_NAME VARCHAR);
INSERT INTO "dbo"."src_new_accounts" ("ACCT_NAME") VALUES ('acct_name_2');
INSERT INTO "dbo"."src_new_accounts" ("ACCT_NAME") VALUES ('acct_name_3');
INSERT INTO "dbo"."src_new_accounts" ("ACCT_NAME") VALUES ('acct_name_4');
INSERT INTO "dbo"."src_new_accounts" ("ACCT_NAME") VALUES (NULL);
CREATE TABLE IF NOT EXISTS dbo.src_new_contacts(CONTACT_NAME VARCHAR);
INSERT INTO "dbo"."src_new_contacts" ("CONTACT_NAME") VALUES ('contact_name_2');
INSERT INTO "dbo"."src_new_contacts" ("CONTACT_NAME") VALUES ('contact_name_3');
INSERT INTO "dbo"."src_new_contacts" ("CONTACT_NAME") VALUES ('contact_name_4');
INSERT INTO "dbo"."src_new_contacts" ("CONTACT_NAME") VALUES (NULL);
CREATE TABLE IF NOT EXISTS dbo.tgt_accounts(ACCT_ID VARCHAR, ACCT_NAME_O VARCHAR);
CREATE TABLE IF NOT EXISTS dbo.tgt_contacts(CONTACT_ID VARCHAR, CONTACT_NAME_O VARCHAR);
