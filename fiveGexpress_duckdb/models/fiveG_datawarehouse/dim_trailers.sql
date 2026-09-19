{{ config(materialized='table') }}

WITH source AS (
    SELECT
        trailer_id,
        trailer_number,
        trailer_type,
        length_feet,
        vin,
        CAST(
            COALESCE(
                TRY_STRPTIME(CAST(acquisition_date AS VARCHAR), '%m/%d/%Y %H:%M:%S'),
                TRY_STRPTIME(CAST(acquisition_date AS VARCHAR), '%Y-%m-%d'),
                TRY_STRPTIME(CAST(acquisition_date AS VARCHAR), '%m/%d/%Y')
            ) AS DATE
        ) AS acquisition_date,
        status,
        current_location,
        current_localtimestamp() AS insertion_timestamp
    FROM {{ ref('stg_trailers') }}
),

unique_source AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY trailer_id) AS row_num
    FROM source
)

SELECT 
    ROW_NUMBER() OVER (ORDER BY trailer_id) AS trailer_key,
    * EXCLUDE (row_num)
FROM unique_source
WHERE row_num = 1