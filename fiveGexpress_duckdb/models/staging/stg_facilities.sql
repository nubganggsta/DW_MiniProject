with source as (

    select * from {{ source('fivegexpress', 'facilities') }}

),

stg_cleaned as (

    select
        trim(upper(facility_id)) as facility_id,
        initcap(trim(facility_name)) as facility_name,
        trim(upper(facility_type)) as facility_type,
        initcap(trim(city)) as city,
        trim(upper(state)) as state,
        cast(latitude as float64) as latitude,
        cast(longitude as float64) as longitude,
        coalesce(cast(dock_doors as integer), 0) as dock_doors,
        trim(operating_hours) as operating_hours,
        current_localtimestamp() as ingestion_timestamp
    from source

)

select * from stg_cleaned