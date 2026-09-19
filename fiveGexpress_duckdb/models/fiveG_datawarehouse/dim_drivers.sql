{{ config(materialized='table') }}

WITH source AS (
    SELECT
        driver_id,
        first_name,
        last_name,
        CAST(
            COALESCE(
                TRY_STRPTIME(hire_date, '%m/%d/%Y %H:%M:%S'),
                TRY_STRPTIME(hire_date, '%Y-%m-%d'),
                TRY_STRPTIME(hire_date, '%m/%d/%Y')
            ) AS DATE
        ) AS hire_date,
        CAST(
            COALESCE(
                TRY_STRPTIME(termination_date, '%m/%d/%Y %H:%M:%S'),
                TRY_STRPTIME(termination_date, '%Y-%m-%d'),
                TRY_STRPTIME(termination_date, '%m/%d/%Y')
            ) AS DATE
        ) AS termination_date,
        license_state,
        CAST(
            COALESCE(
                TRY_STRPTIME(date_of_birth, '%m/%d/%Y %H:%M:%S'),
                TRY_STRPTIME(date_of_birth, '%Y-%m-%d'),
                TRY_STRPTIME(date_of_birth, '%m/%d/%Y')
            ) AS DATE
        ) AS date_of_birth,
        home_terminal,
        employment_status,
        cdl_class,
        years_experience,
        current_localtimestamp() AS insertion_timestamp
    FROM {{ ref('stg_drivers') }}
),

unique_source AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY driver_id) AS row_num
    FROM source
)

SELECT 
    ROW_NUMBER() OVER (ORDER BY driver_id) AS driver_key,
    * EXCLUDE (row_num)
FROM unique_source
WHERE row_num = 1