with stg_drivers as (

    -- อ่านข้อมูลจาก Staging Model เท่านั้น ห้ามอ่านจาก Source โดยตรง
    select * 
    from {{ ref('stg_drivers') }}

),

cleaned as (

    select
        -- Cleansing & Type Casting
        trim(cast(driver_id as string)) as cleaned_driver_id,
        trim(cast(first_name as string)) as cleaned_first_name,
        trim(cast(last_name as string)) as cleaned_last_name,
        cast(hire_date as date) as cleaned_hire_date,
        
        -- Safe NULL Handling for termination_date (ห้ามใส่ค่าปลอม)
        case 
            when cast(termination_date as string) = '' or termination_date is null then null
            else cast(termination_date as date)
        end as cleaned_termination_date,

        upper(trim(cast(license_state as string))) as cleaned_license_state,
        cast(date_of_birth as date) as cleaned_dob,
        trim(cast(home_terminal as string)) as cleaned_home_terminal,
        trim(cast(employment_status as string)) as cleaned_employment_status,
        upper(trim(cast(cdl_class as string))) as cleaned_cdl_class,
        cast(years_experience as integer) as cleaned_years_experience,
        ingestion_timestamp

    from stg_drivers
    where driver_id is not null 
      and trim(cast(driver_id as string)) <> ''

),

deduplicated as (

    select
        *,
        -- Deduplication อ้างอิงตาม Business Key (driver_id)
        row_number() over (
            partition by cleaned_driver_id
            order by cleaned_hire_date desc, ingestion_timestamp desc
        ) as row_num

    from cleaned

),

final as (

    select
        -- สร้าง Surrogate Key ด้วย dbt built-in macro ตามชื่อใน Diagram (driver_key)
        {{ dbt.generate_surrogate_key(['cleaned_driver_id']) }} as driver_key,
        
        -- Business Key และ Attributes ตาม Diagram + full_name สำหรับ Dashboard
        cleaned_driver_id as driver_id,
        cleaned_first_name as first_name,
        cleaned_last_name as last_name,
        
        -- Derived column สำหรับตอบโจทย์ Top 10 Drivers บน BI Tool
        cleaned_first_name || ' ' || cleaned_last_name as full_name,
        
        cleaned_hire_date as hire_date,
        cleaned_termination_date as termination_date,
        cleaned_license_state as license_state,
        cleaned_dob as date_of_birth,
        cleaned_home_terminal as home_terminal,
        cleaned_employment_status as employment_status,
        cleaned_cdl_class as cdl_class,
        cleaned_years_experience as years_experience

    from deduplicated
    where row_num = 1

)

select * 
from final