-- Informatica lookup with unclear multiple-match policy (fail-closed rewrite)
SELECT d.diagnosis_id, p.provider_name
FROM {{ ref('raw_stg_diagnosis') }} d
JOIN {{ source('clinical', 'provider') }} p ON d.provider_id = p.provider_id
