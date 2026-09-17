with source as (

    select * from {{ source('northwind', 'fuel_purchases') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
