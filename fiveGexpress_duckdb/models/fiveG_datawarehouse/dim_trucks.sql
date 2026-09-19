{{ config(materialized='table') }}

WITH source AS (
    SELECT
        truck_id,
        make,
        model_year,
        vin,
        CAST(
            COALESCE(
                TRY_STRPTIME(CAST(acquisition_date AS VARCHAR), '%m/%d/%Y %H:%M:%S'),
                TRY_STRPTIME(CAST(acquisition_date AS VARCHAR), '%Y-%m-%d'),
                TRY_STRPTIME(CAST(acquisition_date AS VARCHAR), '%m/%d/%Y')
            ) AS DATE
        ) AS acquisition_date,
        acquisition_mileage,
        fuel_type,
        tank_capacity_gallons,
        status,
        home_terminal,
        current_localtimestamp() AS insertion_timestamp
    FROM {{ ref('stg_trucks') }}
),

unique_source AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY truck_id) AS row_num
    FROM source
)

SELECT 
    ROW_NUMBER() OVER (ORDER BY truck_id) AS truck_key,
    * EXCLUDE (row_num)
FROM unique_source
WHERE row_num = 1