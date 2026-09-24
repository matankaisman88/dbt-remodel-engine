CREATE OR REPLACE TABLE seed_diagnosis AS
SELECT * FROM (
  VALUES
    (1001, 'E11.9', 'active', 501),
    (1002, 'I10', 'inactive', 502),
    (1003, 'J45.909', 'active', 501)
) AS t(diagnosis_id, diagnosis_code, status, provider_id);

CREATE OR REPLACE TABLE seed_provider AS
SELECT * FROM (
  VALUES
    (501, 'Dr Adams', 1),
    (501, 'Dr Adams Duplicate', 2),
    (502, 'Dr Lee', 1)
) AS t(provider_id, provider_name, provider_rank);

CREATE OR REPLACE TABLE parity_int_diagnosis_enriched AS
SELECT
  d.diagnosis_id,
  d.diagnosis_code,
  d.status,
  p.provider_name
FROM seed_diagnosis d
JOIN (
  SELECT provider_id, provider_name
  FROM (
    SELECT
      provider_id,
      provider_name,
      ROW_NUMBER() OVER (PARTITION BY provider_id ORDER BY provider_rank) AS rn
    FROM seed_provider
  ) x
  WHERE rn = 1
) p ON d.provider_id = p.provider_id;

CREATE OR REPLACE TABLE parity_m_active_diagnosis AS
SELECT
  diagnosis_id,
  diagnosis_code,
  status,
  CASE WHEN status = 'active' THEN TRUE ELSE FALSE END AS is_active
FROM seed_diagnosis
WHERE status = 'active';
