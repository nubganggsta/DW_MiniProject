with routes as (

    select *
    from {{ ref('stg_routes') }}

)

select
    md5(cast(route_id as {{ dbt.type_string() }})) as route_sk,
    route_id,
    origin_city,
    origin_state,
    destination_city,
    destination_state,
    typical_distance_miles,
    base_rate_per_mile,
    fuel_surcharge_rate,
    typical_transit_days,
    ingestion_timestamp as dim_created_at

from routes