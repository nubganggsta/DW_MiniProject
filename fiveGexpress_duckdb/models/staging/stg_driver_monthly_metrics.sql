WITH raw_data AS (
    SELECT
        *,
        CURRENT_TIMESTAMP AS stg_loaded_at,
        'driver_monthly_metrics.csv' AS source_filename,
        'BATCH_2026' AS batch_id
    FROM {{ source('fivegexpress', 'driver_monthly_metrics') }}
),
cleansed AS (
    SELECT
        UPPER(TRIM(CAST(driver_id AS VARCHAR))) AS driver_id,
        TRY_CAST(month AS DATE) AS month,
        COALESCE(TRY_CAST(trips_completed AS INT), 0) AS trips_completed,
        COALESCE(TRY_CAST(total_miles AS INT), 0) AS total_miles,
        COALESCE(TRY_CAST(total_revenue AS DECIMAL(12,2)), 0.00) AS total_revenue,
        COALESCE(TRY_CAST(average_mpg AS FLOAT), 0.0) AS average_mpg,
        COALESCE(TRY_CAST(total_fuel_gallons AS FLOAT), 0.0) AS total_fuel_gallons,
        COALESCE(TRY_CAST(on_time_delivery_rate AS FLOAT), 0.0) AS on_time_delivery_rate,
        COALESCE(TRY_CAST(average_idle_hours AS FLOAT), 0.0) AS average_idle_hours,
        stg_loaded_at,
        source_filename,
        batch_id
    FROM raw_data
),
validated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY driver_id, month
            ORDER BY stg_loaded_at
        ) AS dup_rank
    FROM cleansed
    WHERE driver_id IS NOT NULL
      AND month IS NOT NULL
)
SELECT
    driver_id,
    month,
    trips_completed,
    total_miles,
    total_revenue,
    average_mpg,
    total_fuel_gallons,
    on_time_delivery_rate,
    average_idle_hours,
    stg_loaded_at,
    source_filename,
    batch_id
FROM validated
WHERE dup_rank = 1
