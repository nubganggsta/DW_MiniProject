{{ config(
    materialized = 'table'
) }}

WITH delivery_events AS (

    SELECT
        event_id,
        trip_id,
        load_id,
        facility_id,
        event_type,
        scheduled_datetime,
        actual_datetime,
        detention_minutes,
        on_time_flag
    FROM {{ ref('stg_delivery_events') }}

),

trips AS (

    SELECT
        trip_id,
        driver_id,
        truck_id,
        dispatch_date
    FROM {{ ref('stg_trips') }}

),

loads AS (

    SELECT
        load_id,
        customer_id
    FROM {{ ref('stg_loads') }}

),

source AS (

    SELECT
        de.event_id,
        de.trip_id,
        de.load_id,
        de.facility_id,
        de.event_type,
        de.scheduled_datetime,
        de.actual_datetime,
        de.detention_minutes,
        de.on_time_flag,

        t.driver_id,
        t.truck_id,
        t.dispatch_date,

        l.customer_id

    FROM delivery_events AS de

    LEFT JOIN trips AS t
        ON de.trip_id = t.trip_id

    LEFT JOIN loads AS l
        ON de.load_id = l.load_id

),

fact_delivery AS (

    SELECT

        ROW_NUMBER() OVER (
            ORDER BY s.event_id
        ) AS delivery_event_key,

        s.event_id,

        s.trip_id AS trip_id_degenerate_key,

        s.load_id AS load_id_degenerate_key,

        d.date_key,

        c.customer_key,

        dr.driver_key,

        tr.truck_key,

        f.facility_key,

        s.event_type,

        s.scheduled_datetime AS scheduled_time,

        s.actual_datetime AS actual_time,

        s.detention_minutes AS delay_minutes,

        s.on_time_flag AS is_on_time,

        NOT s.on_time_flag AS is_late,

        s.detention_minutes AS detention,

    FROM source AS s

    LEFT JOIN {{ ref('dim_date') }} AS d
        ON s.dispatch_date = d.full_date

    LEFT JOIN {{ ref('dim_customers') }} AS c
        ON s.customer_id = c.customer_id

    LEFT JOIN {{ ref('dim_drivers') }} AS dr
        ON s.driver_id = dr.driver_id

    LEFT JOIN {{ ref('dim_trucks') }} AS tr
        ON s.truck_id = tr.truck_id

    LEFT JOIN {{ ref('dim_facilities') }} AS f
        ON s.facility_id = f.facility_id

)
SELECT
    delivery_event_key,
    event_id,
    trip_id_degenerate_key,
    load_id_degenerate_key,
    date_key,
    customer_key,
    driver_key,
    truck_key,
    facility_key,
    event_type,
    scheduled_time,
    actual_time,
    delay_minutes,
    is_on_time,
    is_late,
    detention

FROM fact_delivery