with source as (

    select * from {{ source('fivegexpress', 'safety_incidents') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
