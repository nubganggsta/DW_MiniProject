WITH raw_data AS (
    SELECT
        *,
        CURRENT_TIMESTAMP AS stg_loaded_at,
        'fuel_purchases.csv' AS source_filename,
        'BATCH_2026' AS batch_id
    FROM {{ source('fivegexpress', 'fuel_purchases') }}
),
cleansed AS (
    SELECT
        UPPER(TRIM(CAST(fuel_purchase_id AS VARCHAR))) AS fuel_purchase_id,
        UPPER(TRIM(CAST(driver_id AS VARCHAR))) AS driver_id,
        UPPER(TRIM(CAST(truck_id AS VARCHAR))) AS truck_id,
        UPPER(TRIM(CAST(trip_id AS VARCHAR))) AS trip_id,
        TRY_CAST(purchase_date AS DATE) AS purchase_date,
        COALESCE(NULLIF(TRIM(CAST(location_city AS VARCHAR)), ''), 'Unknown') AS location_city,
        UPPER(COALESCE(NULLIF(TRIM(CAST(location_state AS VARCHAR)), ''), 'N/A')) AS location_state,
        COALESCE(TRY_CAST(gallons AS FLOAT), 0.0) AS gallons,
        COALESCE(TRY_CAST(price_per_gallon AS FLOAT), 0.0) AS price_per_gallon,
        COALESCE(TRY_CAST(total_cost AS DECIMAL(10,2)), 0.00) AS total_cost,
        CAST(fuel_card_number AS VARCHAR) AS fuel_card_number,
        stg_loaded_at,
        source_filename,
        batch_id
    FROM raw_data
),
validated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY fuel_purchase_id
            ORDER BY stg_loaded_at
        ) AS dup_rank
    FROM cleansed
    WHERE fuel_purchase_id IS NOT NULL
)
SELECT
    fuel_purchase_id,
    driver_id,
    truck_id,
    trip_id,
    purchase_date,
    location_city,
    location_state,
    gallons,
    price_per_gallon,
    total_cost,
    fuel_card_number,
    stg_loaded_at,
    source_filename,
    batch_id
FROM validated
WHERE dup_rank = 1
