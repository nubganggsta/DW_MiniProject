{{ config(materialized='table', partition_by='purchase_date') }}

WITH source AS (
    SELECT
        fuel_purchase_id,
        CAST(purchase_date AS DATE) AS purchase_date,
        location_city,
        location_state,
        gallons,
        price_per_gallon,
        total_cost,
        truck_id,
        current_localtimestamp() AS insertion_timestamp
    FROM {{ ref('stg_fuel_purchases') }}
),

unique_source AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY fuel_purchase_id) AS row_num
    FROM source
),

cleaned AS (
    SELECT * EXCLUDE (row_num) FROM unique_source WHERE row_num = 1
)

SELECT
    ROW_NUMBER() OVER (ORDER BY c.fuel_purchase_id) AS fuel_key,
    CAST(strftime(c.purchase_date, '%Y%m%d') AS INT) AS date_key,
    tr.truck_key,
    c.total_cost AS fuel_cost,
    c.gallons,
    c.purchase_date,
    c.insertion_timestamp
FROM cleaned c
LEFT JOIN {{ ref('dim_trucks') }} tr ON c.truck_id = tr.truck_id