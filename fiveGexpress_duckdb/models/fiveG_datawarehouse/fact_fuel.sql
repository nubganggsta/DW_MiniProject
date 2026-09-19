SELECT
    MD5(CAST(fuel_purchase_id AS VARCHAR)) AS fuel_key,
    fuel_purchase_id AS fuel_id,
    trip_id AS trip_id_degenerate_key,
    CAST(STRFTIME(purchase_date, '%Y%m%d') AS INT) AS date_key,
    MD5(CAST(truck_id AS VARCHAR)) AS truck_key,
    MD5(CAST(driver_id AS VARCHAR)) AS driver_key,
    gallons,
    price_per_gallon AS price,
    total_cost
FROM {{ ref('stg_fuel_purchases') }}