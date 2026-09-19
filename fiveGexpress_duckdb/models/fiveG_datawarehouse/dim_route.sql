with stg_routes as (

    -- อ่านข้อมูลจาก Staging Model เท่านั้น ห้ามอ่านจาก Source โดยตรง
    select * 
    from {{ ref('stg_routes') }}

),

cleaned as (

    select
        -- Cleansing & Type Casting
        trim(cast(route_id as string)) as cleaned_route_id,
        trim(cast(origin_city as string)) as cleaned_origin_city,
        upper(trim(cast(origin_state as string))) as cleaned_origin_state,
        trim(cast(destination_city as string)) as cleaned_destination_city,
        upper(trim(cast(destination_state as string))) as cleaned_destination_state,
        cast(typical_distance_miles as numeric) as cleaned_typical_distance_miles,
        cast(base_rate_per_mile as numeric) as cleaned_base_rate_per_mile,
        cast(fuel_surcharge_rate as numeric) as cleaned_fuel_surcharge_rate,
        cast(typical_transit_days as numeric) as cleaned_typical_transit_days,
        ingestion_timestamp

    from stg_routes
    -- ตรวจสอบและตัด Record ที่ไม่มี Business Key ออก
    where route_id is not null 
      and trim(cast(route_id as string)) <> ''

),

deduplicated as (

    select
        *,
        -- Deduplication อ้างอิงตาม Business Key (route_id)
        row_number() over (
            partition by cleaned_route_id
            order by ingestion_timestamp desc
        ) as row_num

    from cleaned

),

final as (

    select
        -- สร้าง Surrogate Key ตามชื่อใน Diagram (route_key)
        {{ dbt_utils.generate_surrogate_key(['cleaned_route_id']) }} as route_key,
        
        -- Business Key และ Attribute ทั้งหมดตาม Diagram
        cleaned_route_id as route_id,
        cleaned_origin_city as origin_city,
        cleaned_origin_state as origin_state,
        cleaned_destination_city as destination_city,
        cleaned_destination_state as destination_state,
        cleaned_typical_distance_miles as typical_distance_miles,
        cleaned_base_rate_per_mile as base_rate_per_mile,
        cleaned_fuel_surcharge_rate as fuel_surcharge_rate,
        cleaned_typical_transit_days as typical_transit_days

    from deduplicated
    where row_num = 1

)

select * 
from final