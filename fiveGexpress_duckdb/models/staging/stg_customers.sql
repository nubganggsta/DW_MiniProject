with source as (

    select * from {{ source('northwind', 'customers') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
