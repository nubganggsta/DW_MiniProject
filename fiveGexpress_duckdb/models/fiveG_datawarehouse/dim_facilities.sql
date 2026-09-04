with stg_facilities as (
    select * from {{ ref('stg_facilities') }}
)

select
    md5(cast(facility_id as string)) as facility_key,
    facility_id,
    facility_name,
    city,
    state,
    dock_doors,

from stg_facilities