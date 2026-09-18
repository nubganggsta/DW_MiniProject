with stg_drivers as (

    -- อ่านข้อมูลจาก Staging Model โดยตรง ห้ามอ่านจาก Source
    select * from {{ ref('stg_drivers') }}

),

stg_cleaned as (

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

        trim(cast(license_number as string)) as cleaned_license_number,
        upper(trim(cast(license_state as string))) as cleaned_license_state,
        cast(date_of_birth as date) as cleaned_dob,
        trim(cast(home_terminal as string)) as cleaned_home_terminal,
        coalesce(trim(cast(employment_status as string)), 'Active') as cleaned_employment_status,
        upper(trim(cast(cdl_class as string))) as cleaned_cdl_class,
        coalesce(cast(years_experience as integer), 0) as cleaned_years_experience,
        ingestion_timestamp

    from stg_drivers
    where driver_id is not null 
      and trim(cast(driver_id as string)) <> ''

),

deduplicated as (

    select
        *,
        -- กำจัดข้อมูลซ้ำอ้างอิงตาม driver_id
        row_number() over (
            partition by cleaned_driver_id
            order by cleaned_hire_date desc, ingestion_timestamp desc
        ) as row_num

    from stg_cleaned

),

final as (

    select
        -- สร้าง Surrogate Key ด้วย dbt_utils
        {{ dbt_utils.generate_surrogate_key(['cleaned_driver_id']) }} as Driver_SK,
        cleaned_driver_id as Driver_ID,
        cleaned_first_name as First_Name,
        cleaned_last_name as Last_Name,
        cleaned_hire_date as Hire_Date,
        cleaned_termination_date as Termination_Date,
        cleaned_license_number as License_Number,
        cleaned_license_state as License_State,
        cleaned_dob as Date_Of_Birth,
        cleaned_home_terminal as Home_Terminal,
        cleaned_employment_status as Employment_Status,
        cleaned_cdl_class as CDL_Class,
        cleaned_years_experience as Years_Experience

    from deduplicated
    where row_num = 1

)

select * from final
