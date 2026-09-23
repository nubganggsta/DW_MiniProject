{{ config(materialized='table', partition_by='dispatch_date') }}

WITH source AS (
    SELECT
        t.trip_id AS trip_id,
        CAST(t.Dispatch_date AS DATE) AS dispatch_date,
        t.actual_distance_miles AS actual_distance_miles,
        t.actual_duration_hours AS actual_duration_hours,
        t.fuel_gallons_used AS fuel_gallons_used,
        t.average_mpg AS average_mpg,
        t.idle_time_hours AS idle_time_hours,
        l.revenue AS revenue,
        l.weight_lbs AS weight_lbs,
        l.pieces AS pieces,
        l.accessorial_charges AS accessorial_charges,
        de.detention_minutes AS detention_minutes,
        de.on_time_flag AS on_time_flag,
        t.truck_id AS truck_id,
        t.trailer_id AS trailer_id,
        l.customer_id AS customer_id,
        t.driver_id AS driver_id,
        de.facility_id AS facility_id,
        l.route_id AS route_id, -- เพิ่ม route_id เพื่อนำไป JOIN หา route_key
        current_localtimestamp() AS insertion_timestamp
    FROM {{ ref('stg_trips') }} t
    LEFT JOIN {{ ref('stg_loads') }} l ON t.load_id = l.load_id
    LEFT JOIN {{ ref('stg_delivery_events') }} de ON t.trip_id = de.trip_id
),

unique_source AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY trip_id) AS row_num
    FROM source
),

cleaned AS (
    SELECT * EXCLUDE (row_num) FROM unique_source WHERE row_num = 1
)

SELECT
    -- ปรับการสร้าง Surrogate Key ให้เป็น Hash ตามมาตรฐานข้อ 3
    {{ dbt_utils.generate_surrogate_key(['c.trip_id']) }} AS trip_key,
    CAST(strftime(c.dispatch_date, '%Y%m%d') AS INT) AS date_key,
    r.route_key, -- ดึง route_key จริงจากการ JOIN แทนการใช้ -1
    tr.truck_key,
    tl.trailer_key,
    cust.customer_key,
    f.facility_key,
    d.driver_key,
    1 AS trip_count,
    c.revenue,
    c.weight_lbs,
    c.pieces,
    c.accessorial_charges,
    c.actual_distance_miles,
    c.actual_duration_hours,
    c.fuel_gallons_used,
    c.average_mpg,
    c.idle_time_hours,
    c.detention_minutes,
    c.on_time_flag,
    c.dispatch_date,
    c.insertion_timestamp
FROM cleaned c
LEFT JOIN {{ ref('dim_routes') }} r ON c.route_id = r.route_id
LEFT JOIN {{ ref('dim_trucks') }} tr ON c.truck_id = tr.truck_id
LEFT JOIN {{ ref('dim_trailers') }} tl ON c.trailer_id = tl.trailer_id
LEFT JOIN {{ ref('dim_customers') }} cust ON c.customer_id = cust.customer_id
LEFT JOIN {{ ref('dim_facilities') }} f ON c.facility_id = f.facility_id
LEFT JOIN {{ ref('dim_drivers') }} d ON c.driver_id = d.driver_id