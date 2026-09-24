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

CREATE OR REPLACE TABLE parity_int_sales_enriched AS
SELECT
  il.invoice_line_id,
  il.customer_id,
  CAST(TRIM(c.customer_name) AS VARCHAR) AS customer_name,
  il.extended_price
FROM seed_invoice_lines il
JOIN seed_customers c ON il.customer_id = c.customer_id;

CREATE OR REPLACE TABLE parity_tgt_dim_customer AS
SELECT
  customer_id,
  CAST(TRIM(customer_name) AS VARCHAR) AS customer_name,
  credit_group,
  CASE WHEN credit_group = 'A' THEN 'Preferred' ELSE 'Standard' END AS customer_tier
FROM seed_customers;

CREATE OR REPLACE TABLE parity_tgt_fct_invoice_lines AS
SELECT
  customer_id,
  SUM(extended_price) AS total_extended_price,
  COUNT(*) AS line_count
FROM seed_invoice_lines
GROUP BY customer_id;

CREATE OR REPLACE TABLE parity_passthrough_ref_only AS
SELECT customer_id, customer_name FROM seed_customers;

CREATE OR REPLACE TABLE parity_multi_consumer_window AS
WITH ranked AS (
  SELECT
    customer_id,
    extended_price,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY extended_price DESC) AS rn
  FROM seed_invoice_lines
),
top_line AS (
  SELECT customer_id, extended_price AS top_price
  FROM ranked
  WHERE rn = 1
),
line_count AS (
  SELECT customer_id, COUNT(*) AS cnt
  FROM ranked
  GROUP BY customer_id
)
SELECT t.customer_id, t.top_price, c.cnt
FROM top_line t
JOIN line_count c ON t.customer_id = c.customer_id;
