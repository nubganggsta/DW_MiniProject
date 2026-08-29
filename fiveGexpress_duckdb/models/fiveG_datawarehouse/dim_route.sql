with routes as (

    select *
    from {{ ref('stg_routes') }}

)

select
    route_id,
    origin_city,
    origin_state,
    destination_city,
    destination_state,
    typical_distance_miles,
    base_rate_per_mile,
    fuel_surcharge_rate,
    typical_transit_days,
    ingestion_timestamp

from routes