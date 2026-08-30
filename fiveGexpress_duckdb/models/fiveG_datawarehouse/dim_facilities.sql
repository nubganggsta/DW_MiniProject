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
    concat(coalesce(trim(city), 'N/A'), ', ', upper(coalesce(trim(state), 'N/A'))) as location_full_name,
    
    -- Numerical Attributes & Geospatial (สำหรับโชว์แผนที่ใน Dashboard)
    cast(latitude as float) as latitude,
    cast(longitude as float) as longitude,
    coalesce(cast(dock_doors as int), 0) as dock_doors,
    
    -- Categorical Bins (สำหรับ Filter หรือ Slicer ใน Dashboard)
    case 
        when dock_doors >= 20 then 'Large Hub (20+ Doors)'
        when dock_doors >= 10 then 'Medium Facility (10-19 Doors)'
        when dock_doors > 0  then 'Small Depot (1-9 Doors)'
        else 'No Dock Doors / Unspecified'
    end as facility_size_group,
    
    coalesce(trim(operating_hours), '24/7') as operating_hours

from stg_facilities