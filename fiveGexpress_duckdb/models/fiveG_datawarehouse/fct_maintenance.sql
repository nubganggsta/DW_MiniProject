with maintenance as (

    select *
    from {{ ref('stg_maintenance_records') }}

)

select
    maintenance_id,
    truck_id,
    maintenance_date,
    maintenance_type,
    odometer_reading,
    labor_hours,
    labor_cost,
    parts_cost,
    total_cost,
    facility_location,
    downtime_hours,
    service_description,
    ingestion_timestamp

from maintenance