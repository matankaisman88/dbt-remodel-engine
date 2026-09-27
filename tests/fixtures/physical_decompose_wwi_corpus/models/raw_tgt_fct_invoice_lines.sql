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
)
SELECT
  invoice_line_id,
  customer_id,
  customer_name,
  extended_price,
  credit_group
FROM enriched
