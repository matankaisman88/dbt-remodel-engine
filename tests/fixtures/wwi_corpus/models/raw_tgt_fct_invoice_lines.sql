SELECT
  customer_id,
  SUM(extended_price) AS total_extended_price,
  COUNT(*) AS line_count
FROM {{ source('wwi', 'invoice_lines') }}
GROUP BY customer_id
