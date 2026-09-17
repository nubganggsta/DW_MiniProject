with source as (

    select * from {{ source('fivegexpress', 'trucks') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
