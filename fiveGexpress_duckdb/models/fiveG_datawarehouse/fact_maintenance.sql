{{ config(materialized='table', partition_by='maintenance_date') }}

WITH source AS (
    SELECT
        maintenance_id,
        CAST(maintenance_date AS DATE) AS maintenance_date,
        maintenance_type,
        odometer_reading,
        labor_hours,
        labor_cost,
        parts_cost,
        total_cost,
        downtime_hours,
        truck_id,
        current_localtimestamp() AS insertion_timestamp
    FROM {{ ref('stg_maintenance_records') }}
),

unique_source AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY maintenance_id) AS row_num
    FROM source
),

cleaned AS (
    SELECT * EXCLUDE (row_num) FROM unique_source WHERE row_num = 1
)

SELECT
    ROW_NUMBER() OVER (ORDER BY c.maintenance_id) AS maintenance_key,
    CAST(strftime(c.maintenance_date, '%Y%m%d') AS INT) AS date_key,
    tr.truck_key,
    c.maintenance_type,
    c.labor_cost,
    c.parts_cost,
    c.total_cost AS maintenance_cost,
    c.downtime_hours,
    1 AS maintenance_count,
    c.maintenance_date,
    c.insertion_timestamp
FROM cleaned c
LEFT JOIN {{ ref('dim_trucks') }} tr ON c.truck_id = tr.truck_id