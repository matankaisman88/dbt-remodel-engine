CREATE OR REPLACE TABLE seed_customers AS
SELECT * FROM (
  VALUES
    (1, 'Contoso Ltd', 'A'),
    (2, 'Fabrikam Inc', 'B'),
    (3, NULL, 'A')
) AS t(customer_id, customer_name, credit_group);

CREATE OR REPLACE TABLE seed_invoice_lines AS
SELECT * FROM (
  VALUES
    (101, 1, 10.0),
    (102, 1, 5.0),
    (103, 2, 7.5),
    (104, 3, 2.0)
) AS t(invoice_line_id, customer_id, extended_price);

CREATE OR REPLACE TABLE parity_stg_customers AS
WITH source_rows AS (
  SELECT customer_id, customer_name, credit_group
  FROM seed_customers
),
filtered AS (
  SELECT
    customer_id,
    CAST(TRIM(customer_name) AS VARCHAR) AS customer_name,
    credit_group
  FROM source_rows
  WHERE customer_id IS NOT NULL
)
SELECT * FROM filtered;

CREATE OR REPLACE TABLE parity_tgt_dim_customer AS
WITH invoice_base AS (
  SELECT invoice_line_id, customer_id, extended_price
  FROM seed_invoice_lines
),
enriched AS (
  SELECT
    il.invoice_line_id,
    il.customer_id,
    CAST(TRIM(c.customer_name) AS VARCHAR) AS customer_name,
    il.extended_price,
    c.credit_group
  FROM invoice_base il
  JOIN parity_stg_customers c ON il.customer_id = c.customer_id
),
dim_rows AS (
  SELECT DISTINCT customer_id, customer_name, credit_group
  FROM enriched
)
SELECT
  customer_id,
  customer_name,
  credit_group,
  CASE WHEN credit_group = 'A' THEN 'Preferred' ELSE 'Standard' END AS customer_tier
FROM dim_rows;

CREATE OR REPLACE TABLE parity_tgt_fct_invoice_lines AS
WITH invoice_base AS (
  SELECT invoice_line_id, customer_id, extended_price
  FROM seed_invoice_lines
),
enriched AS (
  SELECT
    il.invoice_line_id,
    il.customer_id,
    CAST(TRIM(c.customer_name) AS VARCHAR) AS customer_name,
    il.extended_price,
    c.credit_group
  FROM invoice_base il
  JOIN parity_stg_customers c ON il.customer_id = c.customer_id
)
SELECT
  invoice_line_id,
  customer_id,
  customer_name,
  extended_price,
  credit_group
FROM enriched;
