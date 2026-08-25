with source as (


    select *
    from {{ source('fiveGexpress', 'maintenance_records') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source