SELECT
  diagnosis_id,
  CAST(diagnosis_code AS VARCHAR) AS diagnosis_code,
  COALESCE(status, 'unknown') AS status,
  provider_id
FROM {{ source('clinical', 'diagnosis') }}
WHERE diagnosis_id IS NOT NULL
