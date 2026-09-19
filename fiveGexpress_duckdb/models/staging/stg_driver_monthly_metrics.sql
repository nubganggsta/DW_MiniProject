with source as (

    select * from {{ source('fivegexpress', 'driver_monthly_metrics') }}
)
select
    *,
    current_localtimestamp() as ingestion_timestamp
from source

