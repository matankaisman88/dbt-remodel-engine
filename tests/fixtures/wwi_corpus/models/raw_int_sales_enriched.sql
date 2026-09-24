WITH invoice_base AS (
  SELECT invoice_line_id, customer_id, extended_price
  FROM {{ source('wwi', 'invoice_lines') }}
),
joined AS (
  SELECT
    il.invoice_line_id,
    il.customer_id,
    CAST(TRIM(c.customer_name) AS VARCHAR) AS customer_name,
    il.extended_price
  FROM invoice_base il
  JOIN {{ ref('raw_stg_customers') }} c ON il.customer_id = c.customer_id
)
SELECT * FROM joined
