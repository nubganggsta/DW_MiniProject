SELECT
    MD5(CAST(maintenance_id AS VARCHAR)) AS maintenance_key,
    maintenance_id,
    MD5(CAST(truck_id AS VARCHAR)) AS truck_key,
    CAST(STRFTIME(maintenance_date, '%Y%m%d') AS INT) AS date_key,
    maintenance_type,
    labor_cost,
    parts_cost,
    total_cost,
    downtime_hours
FROM {{ ref('stg_maintenance_records') }}