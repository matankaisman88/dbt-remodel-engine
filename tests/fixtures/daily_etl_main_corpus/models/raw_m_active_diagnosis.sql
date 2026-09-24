SELECT
  diagnosis_id,
  diagnosis_code,
  status,
  CASE WHEN status = 'active' THEN TRUE ELSE FALSE END AS is_active
FROM {{ ref('raw_stg_diagnosis') }}
WHERE status = 'active'
