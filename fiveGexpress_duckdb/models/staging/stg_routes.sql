with source as (

    select * from {{ source('fivegexpress', 'routes') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
