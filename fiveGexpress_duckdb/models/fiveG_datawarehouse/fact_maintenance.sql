WITH maintenance_records AS (

    SELECT
        maintenance_id,
        truck_id,
        maintenance_date,
        maintenance_type,
        labor_cost,
        parts_cost,
        total_cost,
        downtime_hours
    FROM {{ ref('stg_maintenance_records') }}

),

fact_maintenance AS (

    SELECT

        MD5(CAST(m.maintenance_id AS VARCHAR)) AS maintenance_key,

        m.maintenance_id,

        d.date_key,

        tr.truck_key,

        m.maintenance_type,

        m.labor_cost,

        m.parts_cost,

        m.total_cost,

        m.downtime_hours AS downtime

    FROM maintenance_records AS m

    LEFT JOIN {{ ref('dim_date') }} AS d
        ON m.maintenance_date = d.full_date

    LEFT JOIN {{ ref('dim_trucks') }} AS tr
        ON m.truck_id = tr.truck_id

)

SELECT
    maintenance_key,
    maintenance_id,
    date_key,
    truck_key,
    maintenance_type,
    labor_cost,
    parts_cost,
    total_cost,
    downtime

FROM fact_maintenance
