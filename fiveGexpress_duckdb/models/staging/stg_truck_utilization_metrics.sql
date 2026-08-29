with source as (

    select * from {{ source('fivegexpress', 'truck_utilization_metrics') }}

),

stg_cleaned as (

    select
        trim(upper(truck_id)) as truck_id,
        cast(month as date) as metric_month,
        cast(trips_completed as integer) as trips_completed,
        cast(total_miles as integer) as total_miles,
        cast(total_revenue as numeric(12, 2)) as total_revenue,
        cast(average_mpg as numeric(5, 2)) as average_mpg,
        cast(maintenance_events as integer) as maintenance_events,
        cast(maintenance_cost as numeric(12, 2)) as maintenance_cost,
        cast(downtime_hours as numeric(8, 2)) as downtime_hours,
        cast(utilization_rate as numeric(5, 4)) as utilization_rate,
        current_localtimestamp() as ingestion_timestamp
    from source

)

select * from stg_cleaned