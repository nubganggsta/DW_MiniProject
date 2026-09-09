with stg_facilities as (
    select * from {{ ref('stg_facilities') }}
)

select
    -- Primary Key สำหรับ Join กับ Fact Table
    md5(cast(facility_id as string)) as facility_key,
    
    -- Business Key
    facility_id,
    
    -- Cleaned Text Attributes (พร้อมใช้ใน Dropdown Filter)
    coalesce(trim(facility_name), 'Unknown Facility') as facility_name,
    coalesce(trim(city), 'N/A') as city,
    upper(coalesce(trim(state), 'N/A')) as state,

    coalesce(cast(dock_doors as int), 0) as dock_doors,

from stg_facilities