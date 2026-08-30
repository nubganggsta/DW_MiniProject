{{ config(
    materialized='table'
) }}

with date_spine as (
    -- ใช้ generate_series สำหรับ DuckDB เพื่อสร้างวันที่ตั้งแต่ 1950 ถึง 2030
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
        -- Date Key (เช่น 19500101, 20260829)
        cast(strftime(date_day, '%Y%m%d') as int) as date_key,
        
        -- Full Date
        date_day as full_date,
        
        -- Year Attributes
        year(date_day) as year,
        year(date_day) as iso_year,
        
        -- Quarter Attributes
        quarter(date_day) as quarter,
        concat('Q', quarter(date_day)) as quarter_name,
        concat(year(date_day), '-Q', quarter(date_day)) as year_quarter,
        
        -- Month Attributes
        month(date_day) as month,
        strftime(date_day, '%B') as month_name,       -- e.g., 'August'
        strftime(date_day, '%b') as month_name_short,  -- e.g., 'Aug'
        strftime(date_day, '%Y-%m') as year_month,    -- e.g., '2026-08'
        
        -- Week Attributes
        weekofyear(date_day) as week_of_year,
        weekofyear(date_day) as iso_week_of_year,
        
        -- Day Attributes
        dayofmonth(date_day) as day_of_month,
        dayofweek(date_day) as day_of_week,
        strftime(date_day, '%a') as day_name_short,    -- e.g., 'Sat'
        strftime(date_day, '%A') as day_name,          -- e.g., 'Saturday'
        
        -- Flags
        case when dayofweek(date_day) in (0, 6) then true else false end as is_weekend,
        case when dayofweek(date_day) between 1 and 5 then true else false end as is_weekday,
        case when date_day = last_day(date_day) then true else false end as is_month_end,
        case when dayofmonth(date_day) = 1 then true else false end as is_month_start

    from date_spine
)

select * from dim_date_calculated