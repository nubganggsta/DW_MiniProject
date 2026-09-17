with source as (

    select * from {{ source('northwind', 'routes') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
