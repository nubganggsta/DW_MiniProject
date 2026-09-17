with source as (

    select * from {{ source('fivegexpress', 'fuel_purchases') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
