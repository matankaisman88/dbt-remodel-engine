WITH ranked AS (
  SELECT
    customer_id,
    extended_price,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY extended_price DESC) AS rn
  FROM {{ source('wwi', 'invoice_lines') }}
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
JOIN line_count c ON t.customer_id = c.customer_id
