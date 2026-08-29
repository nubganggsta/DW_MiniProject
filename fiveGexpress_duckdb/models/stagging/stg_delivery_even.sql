with source as (

    select *
    from {{ source('fivegexpress', 'delivery_events') }}

),

cleaned as (

    select
        nullif(trim(cast(event_id as varchar)), '') as event_id,
        nullif(trim(cast(trip_id as varchar)), '') as trip_id,
        nullif(trim(cast(load_id as varchar)), '') as load_id,
        nullif(trim(cast(facility_id as varchar)), '') as facility_id,
        nullif(trim(event_type), '') as event_type, 
        
        cast(scheduled_datetime as time) as scheduled_datetime, 
        cast(actual_datetime as time) as actual_datetime,

        case
            when detention_minutes >= 0
                then detention_minutes
            else null
        end as detention_minutes,

        case
            when on_time_flag in (0, 1)
                then on_time_flag
            else null
        end as on_time_flag,

        nullif(trim(location_city), '') as location_city,
        nullif(trim(location_state), '') as location_state,

        -- Metadata
        current_localtimestamp() as ingestion_timestamp

    from source

)

select *
from cleaned