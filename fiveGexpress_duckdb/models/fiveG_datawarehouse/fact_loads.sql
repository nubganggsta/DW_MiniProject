{{ config(
materialized = 'table'
) }}

WITH source AS (

SELECT
    load_id,
    customer_id,
    route_id,
    load_date,
    weight_lbs,
    pieces,
    revenue,
    fuel_surcharge,
    accessorial_charges
FROM {{ ref('stg_loads') }}
),

fact_loads AS (
SELECT
    ROW_NUMBER() OVER (
        ORDER BY s.load_id
    ) AS load_key,
    s.load_id AS load_id,
    d.date_key,
    c.customer_key,
    r.route_key,
    1 AS load_count,
    s.weight_lbs AS weight,
    s.pieces,
    s.revenue,
    s.fuel_surcharge,
    s.accessorial_charges

FROM source AS s

LEFT JOIN {{ ref('dim_date') }} AS d
    ON s.load_date = d.full_date

LEFT JOIN {{ ref('dim_customers') }} AS c
    ON s.customer_id = c.customer_id

LEFT JOIN {{ ref('dim_route') }} AS r
    ON s.route_id = r.route_id
)

SELECT
load_key,
load_id,
date_key,
customer_key,
route_key,
load_count,
weight,
pieces,
revenue,
fuel_surcharge,
accessorial_charges

FROM fact_loads
