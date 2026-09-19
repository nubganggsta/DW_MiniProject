with source as (

    select * from {{ source('fivegexpress', 'truck_utilization_metrics') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source
