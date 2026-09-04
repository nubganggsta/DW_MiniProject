{{ config(
    materialized='table'
) }}

with date_spine as (

    -- ใช้ generate_series สำหรับ DuckDB
    -- สร้างวันที่ตั้งแต่ 1950-01-01 ถึง 2030-12-31
    select
        cast(generate_series as date) as date_day
    from generate_series(
        date '1950-01-01',
        date '2030-12-31',
        interval '1 day'
    )

),

dim_date_calculated as (

    select

        -- Date Key เช่น 19500101, 20260829
        cast(strftime(date_day, '%Y%m%d') as int) as date_key,

        -- Full Date
        date_day as full_date,

        -- Day
        dayofmonth(date_day) as day,

        -- Month
        month(date_day) as month,

        -- Month Name เช่น January, August
        strftime(date_day, '%B') as month_name,

        -- Quarter
        quarter(date_day) as quarter,

        -- Year
        year(date_day) as year

    from date_spine

)

select *
from dim_date_calculated