with source as (
    select *
    from read_csv_auto('datasets/routes.csv', header = true, nullstr = '')
), cleaned as (
    select
        nullif(trim(route_id), '') as route_id,
        nullif(trim(origin_city), '') as origin_city,
        nullif(trim(origin_state), '') as origin_state,
        nullif(trim(destination_city), '') as destination_city,
        nullif(trim(destination_state), '') as destination_state,
        try_cast(typical_distance_miles as double) as typical_distance_miles,
        try_cast(base_rate_per_mile as double) as base_rate_per_mile,
        try_cast(fuel_surcharge_rate as double) as fuel_surcharge_rate,
        try_cast(typical_transit_days as integer) as typical_transit_days,
        current_localtimestamp() as ingestion_timestamp
    from source
    where nullif(trim(route_id), '') is not null
    qualify row_number() over (
        partition by trim(route_id)
        order by trim(route_id)
    ) = 1
)
select * from cleaned