{{ config(
    materialized='table'
) }}

with stg_trucks as (

    select * 
    from {{ ref('stg_trucks') }}

)

select
    -- Primary Key (Surrogate Key)
    md5(cast(truck_id as {{ dbt.type_string() }})) as Truck_Key,

    -- Business Key & Attributes
    truck_id as Truck_ID,
    unit_number as Unit_Number,
    make as Make,
    cast(model_year as int) as Model_Year,
    vin as VIN,
    fuel_type as Fuel_Type,
    status as Status,
    home_terminal as Home_Terminal

from stg_trucks