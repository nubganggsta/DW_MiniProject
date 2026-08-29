with source as (

    select * from {{ source('fivegexpress', 'fuel_purchases') }}

),

stg_cleaned as (

    select
        -- Primary Key & Foreign Keys: ตัด space และปรับเป็นตัวพิมพ์ใหญ่ (คงค่า NULL ไว้ตามเดิม)
        trim(upper(fuel_purchase_id)) as fuel_purchase_id,
        trim(upper(trip_id)) as trip_id,
        trim(upper(truck_id)) as truck_id,
        trim(upper(driver_id)) as driver_id,

        -- แปลงเป็นประเภท Date
        cast(purchase_date as date) as purchase_date,

        -- ตัด space และปรับตัวอักษร
        initcap(trim(location_city)) as location_city,
        trim(upper(location_state)) as location_state,
        trim(fuel_card_number) as fuel_card_number,

        -- Numeric: แปลงประเภทตัวเลขทศนิยม
        cast(gallons as float64) as gallons,
        cast(price_per_gallon as float64) as price_per_gallon,
        cast(total_cost as float64) as total_cost,

        current_localtimestamp() as ingestion_timestamp
    from source

)

select * from stg_cleaned