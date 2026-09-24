SELECT customer_id, customer_name
FROM {{ ref('raw_stg_customers') }}
