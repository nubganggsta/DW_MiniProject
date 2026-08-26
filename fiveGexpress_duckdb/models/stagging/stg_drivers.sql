with source as (

    select * from {{ source('fivegexpress', 'drivers') }}

),

stg_cleaned as (

    select
        trim(upper(driver_id)) as driver_id,
        trim(first_name) as first_name,
        trim(last_name) as last_name,
        cast(hire_date as date) as hire_date,
        cast(termination_date as date) as termination_date,
        cast(date_of_birth as date) as date_of_birth,
        trim(upper(license_number)) as license_number,
        trim(upper(license_state)) as license_state,
        trim(upper(home_terminal)) as home_terminal,
        trim(employment_status) as employment_status,
        trim(upper(cdl_class)) as cdl_class,
        cast(years_experience as integer) as years_experience,
        current_localtimestamp() as ingestion_timestamp
    from source

)

select * from stg_cleaned