with stg_trucks as (

    -- อ่านข้อมูลจาก Staging Model เท่านั้น ห้ามอ่านจาก Source โดยตรง
    select * 
    from {{ ref('stg_trucks') }}

),

cleaned as (

    select
        -- Cleansing & Type Casting
        trim(cast(truck_id as string)) as cleaned_truck_id,
        cast(unit_number as integer) as cleaned_unit_number,
        trim(cast(make as string)) as cleaned_make,
        cast(model_year as integer) as cleaned_model_year,
        trim(cast(vin as string)) as cleaned_vin,
        cast(acquisition_date as date) as cleaned_acquisition_date,
        cast(acquisition_mileage as integer) as cleaned_acquisition_mileage,
        trim(cast(fuel_type as string)) as cleaned_fuel_type,
        cast(tank_capacity_gallons as integer) as cleaned_tank_capacity_gallons,
        trim(cast(status as string)) as cleaned_status,
        trim(cast(home_terminal as string)) as cleaned_home_terminal,
        ingestion_timestamp

    from stg_trucks
    -- ตรวจสอบและตัด Record ที่ไม่มี Business Key ออก
    where truck_id is not null 
      and trim(cast(truck_id as string)) <> ''

),

deduplicated as (

    select
        *,
        -- Deduplication อ้างอิงตาม Business Key (truck_id)
        row_number() over (
            partition by cleaned_truck_id
            order by cleaned_acquisition_date desc, ingestion_timestamp desc
        ) as row_num

    from cleaned

),

final as (

    select
        -- สร้าง Surrogate Key ตามชื่อใน Diagram (truck_key)
        {{ dbt_utils.generate_surrogate_key(['cleaned_truck_id']) }} as truck_key,
        
        -- Business Key และ Attribute ทั้งหมดตาม Diagram (snake_case)
        cleaned_truck_id as truck_id,
        cleaned_make as make,
        cleaned_model_year as model_year,
        cleaned_vin as vin,
        cleaned_acquisition_date as acquisition_date,
        cleaned_acquisition_mileage as acquisition_mileage,
        cleaned_fuel_type as fuel_type,
        cleaned_tank_capacity_gallons as tank_capacity_gallons,
        cleaned_status as status,
        cleaned_home_terminal as home_terminal

    from deduplicated
    where row_num = 1

)

select * 
from final