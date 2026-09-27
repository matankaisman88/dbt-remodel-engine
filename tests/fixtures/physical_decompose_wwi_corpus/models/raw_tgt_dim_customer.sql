WITH invoice_base AS (
  SELECT invoice_line_id, customer_id, extended_price
  FROM {{ source('wwi', 'invoice_lines') }}
),
enriched AS (
  SELECT
    il.invoice_line_id,
    il.customer_id,
    CAST(TRIM(c.customer_name) AS VARCHAR) AS customer_name,
    il.extended_price,
    c.credit_group
  FROM invoice_base il
  JOIN {{ ref('raw_stg_customers') }} c ON il.customer_id = c.customer_id
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
FROM dim_rows
