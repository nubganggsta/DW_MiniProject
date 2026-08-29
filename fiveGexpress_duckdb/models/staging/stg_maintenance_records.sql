with raw as (
    select *
    from read_csv_auto('{{ target.path | replace("/dev.duckdb", "/datasets/maintenance_records.csv") }}', header = true, nullstr = '')
), cleaned as (
    select
        nullif(trim(maintenance_id), '') as maintenance_id,
        nullif(trim(truck_id), '') as truck_id,
        try_cast(maintenance_date as date) as maintenance_date,
        nullif(trim(maintenance_type), '') as maintenance_type,
        try_cast(odometer_reading as bigint) as odometer_reading,
        try_cast(labor_hours as double) as labor_hours,
        try_cast(labor_cost as double) as labor_cost,
        try_cast(parts_cost as double) as parts_cost,
        round(coalesce(try_cast(labor_cost as double), 0) + coalesce(try_cast(parts_cost as double), 0), 2) as total_cost,
        nullif(trim(facility_location), '') as facility_location,
        try_cast(downtime_hours as double) as downtime_hours,
        nullif(trim(service_description), '') as service_description,
        current_localtimestamp() as ingestion_timestamp
    from raw
    where nullif(trim(maintenance_id), '') is not null
    qualify row_number() over (
        partition by trim(maintenance_id)
        order by try_cast(maintenance_date as date) desc
    ) = 1
)
select * from cleaned