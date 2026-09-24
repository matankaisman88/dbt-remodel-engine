-- LOOKUP:prov
WITH diagnosis AS (
  SELECT * FROM {{ ref('raw_stg_diagnosis') }}
),
provider_lookup AS (
  SELECT provider_id, provider_name, provider_rank
  FROM {{ source('clinical', 'provider') }}
)
SELECT
  d.diagnosis_id,
  d.diagnosis_code,
  d.status,
  prov.provider_name
FROM diagnosis d
JOIN provider_lookup prov ON d.provider_id = prov.provider_id
