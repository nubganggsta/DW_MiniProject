with raw as (
    select *
    from {{ source('fivegexpress', 'routes') }}
), 

cleaned as (
    select
        nullif(trim(upper(cast(route_id as varchar))), '') as route_id,
        nullif(trim(cast(origin_city as varchar)), '') as origin_city,
        nullif(trim(cast(origin_state as varchar)), '') as origin_state,
        nullif(trim(cast(destination_city as varchar)), '') as destination_city,
        nullif(trim(cast(destination_state as varchar)), '') as destination_state,
        try_cast(typical_distance_miles as double) as typical_distance_miles,
        try_cast(base_rate_per_mile as double) as base_rate_per_mile,
        try_cast(fuel_surcharge_rate as double) as fuel_surcharge_rate,
        try_cast(typical_transit_days as integer) as typical_transit_days,
        current_localtimestamp() as ingestion_timestamp
    from raw
    where nullif(trim(cast(route_id as varchar)), '') is not null
    qualify row_number() over (
        partition by trim(cast(route_id as varchar))
        order by trim(cast(route_id as varchar))
    ) = 1
)

select * from cleaned