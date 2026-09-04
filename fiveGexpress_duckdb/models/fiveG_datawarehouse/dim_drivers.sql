with stg_drivers as (
    select * from {{ ref('stg_drivers') }}
),

dim_calculated as (
    select
        md5(cast(driver_id as {{ dbt.type_string() }})) as driver_key,
        driver_id,
        concat(coalesce(first_name, ''), ' ', coalesce(last_name, '')) as full_name,
        first_name,
        last_name,
        
        case 
            when termination_date is null and lower(employment_status) = 'active' then true 
            else false 
        end as is_active,
        
        employment_status,
        hire_date,
        termination_date,
        
        -- แก้ไข: เพิ่ม 'day' เป็น Parameter แรก และสลับตำแหน่ง start_date, end_date
        round(
            datediff(
                'day', 
                hire_date, 
                coalesce(termination_date, current_date())
            ) / 365.25, 2
        ) as tenure_years,
        
        date_of_birth,
        
        -- แก้ไข: เพิ่ม 'day' ในการคำนวณอายุ
        floor(datediff('day', date_of_birth, current_date()) / 365.25) as age,
        
        years_experience,
        license_number,
        license_state,
        cdl_class,
        home_terminal

    from stg_drivers
)

select * from dim_calculated