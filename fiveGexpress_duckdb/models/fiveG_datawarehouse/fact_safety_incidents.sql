{{ config(materialized='table', partition_by='incident_date') }}

WITH source AS (

    SELECT

        incident_id,
        trip_id,
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

    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY incident_id
            ORDER BY incident_date DESC
        ) AS row_num

    FROM source

),

cleaned AS (

    SELECT
        * EXCLUDE (row_num)

    FROM unique_source

    WHERE row_num = 1

),

trip_lookup AS (

    SELECT
        trip_id,
        load_id

    FROM (

        SELECT
            trip_id,
            load_id,
            ROW_NUMBER() OVER (
                PARTITION BY trip_id
                ORDER BY trip_id
            ) AS row_num

        FROM {{ ref('stg_trips') }}

    )

    WHERE row_num = 1

),

load_lookup AS (

    SELECT
        load_id,
        route_id

    FROM (

        SELECT
            load_id,
            route_id,
            ROW_NUMBER() OVER (
                PARTITION BY load_id
                ORDER BY load_id
            ) AS row_num

        FROM {{ ref('stg_loads') }}

    )

    WHERE row_num = 1

),

final AS (

    SELECT

        ROW_NUMBER() OVER (
            ORDER BY c.incident_id
        ) AS incident_key,

        CAST(
            strftime(c.incident_date, '%Y%m%d')
            AS INT
        ) AS date_key,

        tr.truck_key,

        d.driver_key,

        r.route_key,

        c.incident_type,

        c.vehicle_damage_cost,

        c.cargo_damage_cost,

        c.claim_amount,

        1 AS incident_count,

        c.incident_date,

        c.insertion_timestamp

    FROM cleaned c

    LEFT JOIN trip_lookup t
        ON c.trip_id = t.trip_id

    LEFT JOIN load_lookup l
        ON t.load_id = l.load_id

    LEFT JOIN {{ ref('dim_routes') }} r
        ON l.route_id = r.route_id

    LEFT JOIN {{ ref('dim_trucks') }} tr
        ON c.truck_id = tr.truck_id

    LEFT JOIN {{ ref('dim_drivers') }} d
        ON c.driver_id = d.driver_id

)

SELECT *
FROM final