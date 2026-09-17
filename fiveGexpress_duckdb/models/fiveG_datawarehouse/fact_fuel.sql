{{ config(
    materialized='table'
) }}

WITH source AS (
    SELECT * FROM {{ ref('stg_fuel_purchases') }}
),

final AS (
    SELECT
        -- Primary Key (Surrogate Key)
        MD5(CAST(fuel_purchase_id AS VARCHAR)) AS fuel_key,
        
        -- Business Key & Degenerate Key
        fuel_purchase_id,
        trip_id AS trip_id_degenerate_key,
        
        -- Date Key (Format YYYYMMDD)
        CAST(STRFTIME(purchase_date, '%Y%m%d') AS INT) AS date_key,
        
        -- Foreign Keys (ป้องกันการเกิด Hash บนค่า NULL)
        CASE 
            WHEN truck_id IS NOT NULL THEN MD5(CAST(truck_id AS VARCHAR)) 
            ELSE NULL 
        END AS truck_key,
        
        CASE 
            WHEN driver_id IS NOT NULL THEN MD5(CAST(driver_id AS VARCHAR)) 
            ELSE NULL 
        END AS driver_key,
        
        -- Measures (คำนวณตัวเลขและล็อก Type ให้แม่นยำ)
        COALESCE(CAST(gallons AS DECIMAL(10, 2)), 0.00) AS gallons,
        COALESCE(CAST(price_per_gallon AS DECIMAL(10, 2)), 0.00) AS price,
        
        -- คำนวณ total_cost หากใน Staging เป็น NULL จะใช้ (gallons * price) แทน
        CAST(
            COALESCE(
                total_cost, 
                COALESCE(gallons, 0) * COALESCE(price_per_gallon, 0)
            ) AS DECIMAL(12, 2)
        ) AS total_cost

    FROM source
)

SELECT * FROM final