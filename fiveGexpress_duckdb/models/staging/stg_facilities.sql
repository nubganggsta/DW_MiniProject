with source as (

    select * from {{ source('northwind', 'facilities') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
