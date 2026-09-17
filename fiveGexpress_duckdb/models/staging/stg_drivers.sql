with source as (

    select * from {{ source('northwind', 'drivers') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
