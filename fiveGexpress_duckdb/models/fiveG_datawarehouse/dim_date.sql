{{ config(materialized='table') }}

WITH date_spine AS (
    SELECT d
    FROM generate_series(DATE '2022-01-01', DATE '2024-12-31', INTERVAL 1 DAY) AS t(d)
),

transformed AS (
    SELECT
        CAST(strftime(d, '%Y%m%d') AS INT) AS date_key,
        d AS full_date,
        CAST(date_part('year', d) AS INT) AS year,
        CAST(date_part('quarter', d) AS INT) AS quarter,
        CAST(date_part('month', d) AS INT) AS month,
        monthname(d) AS month_name,
        dayname(d) AS day_name,
        CASE
            WHEN date_part('dow', d) IN (0, 6) THEN TRUE
            ELSE FALSE
        END AS weekend
    FROM date_spine
)

SELECT * FROM transformed