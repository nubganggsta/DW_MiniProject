with stg_facilities as (

    select * from {{ ref('stg_facilities') }}

),

cleaned as (

    select
        -- Business Key
        trim(cast(facility_id as string)) as facility_id,

        -- Attributes
        trim(cast(facility_name as string)) as facility_name,
        trim(cast(facility_type as string)) as facility_type,
        trim(cast(city as string)) as city,
        upper(trim(cast(state as string))) as state,
        cast(latitude as numeric) as latitude,
        cast(longitude as numeric) as longitude,
        cast(dock_doors as integer) as dock_doors,
        trim(cast(operating_hours as string)) as operating_hours,
        ingestion_timestamp

    from stg_facilities
    where facility_id is not null 
      and trim(cast(facility_id as string)) <> ''

),

deduplicated as (

    select
        *,
        row_number() over (
            partition by facility_id
            order by ingestion_timestamp desc
        ) as row_num

    from cleaned

),

final as (

    select
        -- Primary Key (Surrogate Key) Aligned with Diagram
        {{ dbt.generate_surrogate_key(['facility_id']) }} as facility_key,
        
        -- Diagram Attributes
        facility_id,
        facility_name,
        facility_type,
        city,
        state,
        latitude,
        longitude,
        dock_doors,
        operating_hours

    from deduplicated
    where row_num = 1

)

select * from final