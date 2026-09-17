with source as (

    select * from {{ source('fivegexpress', 'facilities') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
