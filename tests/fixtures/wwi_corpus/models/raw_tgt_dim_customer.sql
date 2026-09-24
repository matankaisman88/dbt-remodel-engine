SELECT
  customer_id,
  CAST(TRIM(customer_name) AS VARCHAR) AS customer_name,
  credit_group,
  CASE WHEN credit_group = 'A' THEN 'Preferred' ELSE 'Standard' END AS customer_tier
FROM {{ source('wwi', 'customers') }}
