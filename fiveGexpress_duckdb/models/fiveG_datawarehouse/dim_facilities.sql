{{ config(materialized='table') }}

WITH source AS (
    SELECT
        facility_id,
        facility_name,
        facility_type,
        city,
        state,
        latitude,
        longitude,
        dock_doors,
        operating_hours,
        current_localtimestamp() AS insertion_timestamp
    FROM {{ ref('stg_facilities') }}
),

unique_source AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY facility_id) AS row_num
    FROM source
)

SELECT 
    ROW_NUMBER() OVER (ORDER BY facility_id) AS facility_key,
    * EXCLUDE (row_num)
FROM unique_source
WHERE row_num = 1