WITH source_rows AS (
  SELECT
    customer_id,
    customer_name,
    credit_group
  FROM {{ source('wwi', 'customers') }}
),
filtered AS (
  SELECT
    customer_id,
    CAST(TRIM(customer_name) AS VARCHAR) AS customer_name,
    credit_group
  FROM source_rows
  WHERE customer_id IS NOT NULL
)
SELECT * FROM filtered
