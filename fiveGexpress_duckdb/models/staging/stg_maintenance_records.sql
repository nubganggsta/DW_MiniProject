with raw as (
    select *
    from {{ source('fivegexpress', 'maintenance_records') }}
), 

cleaned as (
    select
        nullif(trim(cast(maintenance_id as varchar)), '') as maintenance_id,
        nullif(trim(cast(truck_id as varchar)), '') as truck_id,
        try_cast(maintenance_date as date) as maintenance_date,
        nullif(trim(cast(maintenance_type as varchar)), '') as maintenance_type,
        try_cast(odometer_reading as bigint) as odometer_reading,
        try_cast(labor_hours as double) as labor_hours,
        try_cast(labor_cost as double) as labor_cost,
        try_cast(parts_cost as double) as parts_cost,
        round(coalesce(try_cast(labor_cost as double), 0) + coalesce(try_cast(parts_cost as double), 0), 2) as total_cost,
        nullif(trim(cast(facility_location as varchar)), '') as facility_location,
        try_cast(downtime_hours as double) as downtime_hours,
        nullif(trim(cast(service_description as varchar)), '') as service_description,
        current_localtimestamp() as ingestion_timestamp
    from raw
    where nullif(trim(cast(maintenance_id as varchar)), '') is not null
    qualify row_number() over (
        partition by trim(cast(maintenance_id as varchar))
        order by try_cast(maintenance_date as date) desc
    ) = 1
)

select * from cleaned