with stg_drivers as (

    select *
    from {{ ref('stg_drivers') }}

),

dim_calculated as (

    select

        -- Driver Surrogate Key
        md5(cast(driver_id as {{ dbt.type_string() }})) as driver_key,

        -- Driver ID
        driver_id,

        -- Driver Name
        concat(
            coalesce(first_name, ''),
            ' ',
            coalesce(last_name, '')
        ) as full_name,

        -- Hire Date
        hire_date,

        -- Termination Date
        termination_date,

        -- License
        license_number as license,

        -- Home Terminal
        home_terminal,

        -- Experience in years
        round(
            datediff(
                'day',
                hire_date,
                coalesce(termination_date, current_date())
            ) / 365.25,
            2
        ) as experience

    from stg_drivers

)

select *
from dim_calculated