{{ config(materialized='table') }}

WITH source AS (
    SELECT
        route_id,
        origin_city,
        origin_state,
        destination_city,
        destination_state,
        typical_distance_miles,
        base_rate_per_mile,
        fuel_surcharge_rate,
        typical_transit_days,
        current_localtimestamp() AS insertion_timestamp
    FROM {{ ref('stg_routes') }}
),

unique_source AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY route_id) AS row_num
    FROM source
)

SELECT 
    ROW_NUMBER() OVER (ORDER BY route_id) AS route_key,
    * EXCLUDE (row_num)
FROM unique_source
WHERE row_num = 1