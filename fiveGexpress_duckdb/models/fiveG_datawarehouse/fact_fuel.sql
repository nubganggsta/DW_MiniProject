WITH fuel_purchases AS (

    SELECT
        fuel_purchase_id,
        trip_id,
        truck_id,
        driver_id,
        purchase_date,
        gallons,
        price_per_gallon,
        total_cost
    FROM {{ ref('stg_fuel_purchases') }}

),

fact_fuel AS (

    SELECT

        MD5(CAST(fp.fuel_purchase_id AS VARCHAR)) AS fuel_key,

        fp.fuel_purchase_id AS fuel_id,

        fp.trip_id AS trip_id_degenerate_key,

        d.date_key,

        tr.truck_key,

        dr.driver_key,

        fp.gallons,

        fp.price_per_gallon AS price,

        fp.total_cost

    FROM fuel_purchases AS fp

    LEFT JOIN {{ ref('dim_date') }} AS d
        ON fp.purchase_date = d.full_date

    LEFT JOIN {{ ref('dim_trucks') }} AS tr
        ON fp.truck_id = tr.truck_id

    LEFT JOIN {{ ref('dim_drivers') }} AS dr
        ON fp.driver_id = dr.driver_id

)

SELECT
    fuel_key,
    fuel_id,
    trip_id_degenerate_key,
    date_key,
    truck_key,
    driver_key,
    gallons,
    price,
    total_cost

FROM fact_fuel
