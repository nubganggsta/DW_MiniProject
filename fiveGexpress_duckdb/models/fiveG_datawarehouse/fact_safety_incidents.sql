{{ config(materialized='table', partition_by='incident_date') }}

WITH source AS (
    SELECT
        incident_id,
        CAST(incident_date AS DATE) AS incident_date,
        incident_type,
        at_fault_flag,
        injury_flag,
        vehicle_damage_cost,
        cargo_damage_cost,
        claim_amount,
        preventable_flag,
        truck_id,
        driver_id,
        current_localtimestamp() AS insertion_timestamp
    FROM {{ ref('stg_safety_incidents') }}
),

unique_source AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY incident_id) AS row_num
    FROM source
),

cleaned AS (
    SELECT * EXCLUDE (row_num) FROM unique_source WHERE row_num = 1
)

SELECT
    ROW_NUMBER() OVER (ORDER BY c.incident_id) AS incident_key,
    CAST(strftime(c.incident_date, '%Y%m%d') AS INT) AS date_key,
    tr.truck_key,
    d.driver_key,
    c.incident_type,
    c.vehicle_damage_cost,
    c.cargo_damage_cost,
    c.claim_amount,
    1 AS incident_count,
    c.incident_date,
    c.insertion_timestamp
FROM cleaned c
LEFT JOIN {{ ref('dim_trucks') }} tr ON c.truck_id = tr.truck_id
LEFT JOIN {{ ref('dim_drivers') }} d ON c.driver_id = d.driver_id