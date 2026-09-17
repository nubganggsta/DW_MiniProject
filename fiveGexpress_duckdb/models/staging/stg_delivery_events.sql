with source as (

    select * from {{ source('northwind', 'delivery_events') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
