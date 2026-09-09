with source as (

    select *
    from {{ source('fivegexpress', 'loads') }}

),

cleaned as (

    select
        nullif(trim(upper(cast(load_id as varchar))), '') as load_id,
        nullif(trim(upper(cast(customer_id as varchar))), '') as customer_id,
        nullif(trim(upper(cast(route_id as varchar))), '') as route_id,
        cast(load_date as date) as load_date,
        nullif(trim(load_type), '') as load_type,

        case
            when weight_lbs >= 0
                then weight_lbs
            else null
        end as weight_lbs,

        case
            when pieces >= 0
                then pieces
            else null
        end as pieces,

        case
            when revenue >= 0
                then revenue
            else null
        end as revenue,

        case
            when fuel_surcharge >= 0
                then fuel_surcharge
            else null
        end as fuel_surcharge,

        case
            when accessorial_charges >= 0
                then accessorial_charges
            else null
        end as accessorial_charges,

        nullif(trim(load_status), '') as load_status,

        nullif(trim(booking_type), '') as booking_type,

        current_localtimestamp() as ingestion_timestamp

    from source

)

select *
from cleaned