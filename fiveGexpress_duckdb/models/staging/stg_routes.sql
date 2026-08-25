with source as (


    select *
    from {{ source('fiveGexpress', 'routes') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
