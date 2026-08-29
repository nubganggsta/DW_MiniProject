{{ config(
    materialized='table'
) }}

with stg_drivers as (
    select * from {{ ref('stg_drivers') }}
),

dim_calculated as (
    select
        -- 1. Surrogate Key
        md5(cast(driver_id as {{ dbt.type_string() }})) as driver_sk,
        
        -- 2. Business Key
        driver_id,
        
        -- 3. Name Attributes
        concat(coalesce(first_name, ''), ' ', coalesce(last_name, '')) as full_name,
        first_name,
        last_name,
        
        -- 4. Status Flag
        case 
            when termination_date is null and lower(employment_status) = 'active' then true 
            else false 
        end as is_active,
        
        employment_status,
        hire_date,
        termination_date,
        
        -- 5. Tenure Calculation (ปรับการรองรับกรณีวันติดลบ/ทศนิยม)
        round(
            datediff(
                coalesce(termination_date, current_date()), 
                hire_date
            ) / 365.25, 2
        ) as tenure_years,
        
        date_of_birth,
        
        -- 6. Age Calculation (ปัดเศษลงเป็นจำนวนเต็ม)
        floor(datediff(current_date(), date_of_birth) / 365.25) as age,
        
        years_experience,
        license_number,
        license_state,
        cdl_class,
        home_terminal

    from stg_drivers
)

select * from dim_calculated