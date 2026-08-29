with source as (

    select * from {{ source('fivegexpress', 'trucks') }}

),

stg_cleaned as (

    select
        trim(upper(cast(truck_id as varchar))) as truck_id,
        try_cast(unit_number as integer) as unit_number,
        trim(cast(make as varchar)) as make,
        try_cast(model_year as integer) as model_year,
        trim(upper(cast(vin as varchar))) as vin,
        try_cast(acquisition_date as date) as acquisition_date,
        try_cast(acquisition_mileage as integer) as acquisition_mileage,
        trim(cast(fuel_type as varchar)) as fuel_type,
        try_cast(tank_capacity_gallons as integer) as tank_capacity,
        trim(cast(status as varchar)) as status,
        trim(upper(cast(home_terminal as varchar))) as home_terminal,
        current_localtimestamp() as ingestion_timestamp
    from source

)

select * from stg_cleaned