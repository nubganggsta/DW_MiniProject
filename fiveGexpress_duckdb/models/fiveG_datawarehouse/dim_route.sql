with routes as (

    select *
    from {{ ref('stg_routes') }}

)

select
    md5(cast(route_id as {{ dbt.type_string() }})) as route_key,
    route_id,
    origin_city,
    origin_state,
    destination_city,
    destination_state,
    typical_distance_miles as distance,
    base_rate_per_mile as base_rate,
    fuel_surcharge_rate as fuel_surcharge,
    typical_transit_days as transit_days,

from routes