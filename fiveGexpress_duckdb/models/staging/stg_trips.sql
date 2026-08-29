with source as (

    select *
    from {{ source('fivegexpress', 'trips') }}

),

cleaned as (

    select
        nullif(trim(cast(trip_id as varchar)), '') as trip_id,
        nullif(trim(cast(driver_id as varchar)), '') as driver_id,
        nullif(trim(cast(truck_id as varchar)), '') as truck_id,
        nullif(trim(cast(trailer_id as varchar)), '') as trailer_id,
        nullif(trim(cast(load_id as varchar)), '') as load_id,

        cast(dispatch_date as date) as dispatch_date,

        case
            when actual_distance_miles >= 0
                then actual_distance_miles
            else null
        end as actual_distance_miles,

        case
            when actual_duration_hours >= 0
                then actual_duration_hours
            else null
        end as actual_duration_hours,

        case
            when fuel_gallons_used >= 0
                then fuel_gallons_used
            else null
        end as fuel_gallons_used,

        case
            when average_mpg > 0
                then average_mpg
            else null
        end as average_mpg,

        case
            when idle_time_hours >= 0
                then idle_time_hours
            else null
        end as idle_time_hours,

        nullif(trim(cast(trip_status as varchar)), '') as trip_status,

        current_localtimestamp() as ingestion_timestamp

    from source

)

select *
from cleaned