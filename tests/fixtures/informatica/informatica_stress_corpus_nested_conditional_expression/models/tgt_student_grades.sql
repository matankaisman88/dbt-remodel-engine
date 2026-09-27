-- AUTO-GENERATED STRUCTURAL SUGGESTION — NOT SEMANTICALLY VERIFIED.
-- Manual review required against source mapping logic.
{{
  config(
    materialized = 'table',
    schema = "dbo",
    alias = "tgt_student_grades"
  )
}}
-- Target: TGT_STUDENT_GRADES
-- Informatica Load Order: 1
-- Source Instances: SRC_SCORES
WITH
    sq_sq_scores AS (
SELECT STUDENT_ID, SCORE FROM {{ source('dbo', 'src_scores') }}
),

    int_exp_grade_prep AS (
    SELECT
        base.*,
        CASE WHEN SCORE >= 90 THEN 'A' WHEN SCORE >= 80 THEN 'B' WHEN SCORE >= 70 THEN 'C' WHEN SCORE >= 60 THEN 'D' ELSE 'F' END AS GRADE_LOCAL
    FROM sq_sq_scores base

),

    int_exp_grade AS (
    SELECT
        base.*,
        STUDENT_ID AS STUDENT_ID_O,
        SCORE AS SCORE_O,
        GRADE_LOCAL AS GRADE
    FROM int_exp_grade_prep base

)

SELECT
    STUDENT_ID_O AS STUDENT_ID_O,
    SCORE_O AS SCORE_O,
    GRADE AS GRADE
FROM int_exp_grade

