{{ config(
    materialized='table'
) }}

with stg_trucks as (

    select * 
    from {{ ref('stg_trucks') }}

)

select
    -- 1. Surrogate Key
    md5(cast(truck_id as {{ dbt.type_string() }})) as truck_key,

    -- 2. Business Key
    truck_id,

    -- 3. Attributes
    unit_number,
    make,
    model_year,
    vin,
    acquisition_date,
    acquisition_mileage,
    fuel_type,
    tank_capacity,
    status,
    home_terminal,

    -- 4. Audit Column
    ingestion_timestamp as dim_created_at

from stg_trucks