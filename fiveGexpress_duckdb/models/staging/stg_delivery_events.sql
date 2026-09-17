with source as (

    select * from {{ source('fivegexpress', 'delivery_events') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
