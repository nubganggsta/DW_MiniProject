with source as (

    select * from {{ source('northwind', 'loads') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
