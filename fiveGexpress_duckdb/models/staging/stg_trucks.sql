with source as (

    select * from {{ source('fivegexpress', 'trucks') }}

),

stg_cleaned as (

    select
        trim(upper(truck_id)) as truck_id,
        cast(unit_number as integer) as unit_number,
        trim(make) as make,
        cast(model_year as integer) as model_year,
        trim(upper(vin)) as vin,
        cast(acquisition_date as date) as acquisition_date,
        cast(acquisition_mileage as integer) as acquisition_mileage,
        trim(fuel_type) as fuel_type,
        cast(tank_capacity_gallons as integer) as tank_capacity,
        trim(status) as status,
        trim(upper(home_terminal)) as home_terminal,
        current_localtimestamp() as ingestion_timestamp
    from source

)

select * from stg_cleaned