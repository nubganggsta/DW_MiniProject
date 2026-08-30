{{ config(
materialized = 'table'
) }}


WITH trips AS (




SELECT
    trip_id,
    driver_id,
    truck_id,
    load_id,
    dispatch_date,
    actual_distance_miles,
    idle_time_hours
FROM {{ ref('stg_trips') }}




),


trips_with_customer AS (




SELECT
    t.trip_id,
    t.driver_id,
    t.truck_id,
    t.load_id,
    t.dispatch_date,
    t.actual_distance_miles,
    t.idle_time_hours,
    l.customer_id


FROM trips AS t


LEFT JOIN {{ ref('stg_loads') }} AS l
    ON t.load_id = l.load_id




),


fact_trips AS (




SELECT


    ROW_NUMBER() OVER (
        ORDER BY t.trip_id
    ) AS trip_key,


    t.trip_id,


    t.load_id AS load_id_degenerate_key,


    d.date_key,


    dr.driver_key,


    tr.truck_key,


    c.customer_key,


    1 AS trip_count,


    t.actual_distance_miles AS miles,


    t.idle_time_hours AS downtime


FROM trips_with_customer AS t


LEFT JOIN {{ ref('dim_date') }} AS d
    ON t.dispatch_date = d.full_date


LEFT JOIN {{ ref('dim_drivers') }} AS dr
    ON t.driver_id = dr.driver_id


LEFT JOIN {{ ref('dim_trucks') }} AS tr
    ON t.truck_id = tr.truck_id


LEFT JOIN {{ ref('dim_customers') }} AS c
    ON t.customer_id = c.customer_id




)


SELECT
trip_key,
trip_id,
load_id_degenerate_key,
date_key,
driver_key,
truck_key,
customer_key,
trip_count,
miles,
downtime


FROM fact_trips
