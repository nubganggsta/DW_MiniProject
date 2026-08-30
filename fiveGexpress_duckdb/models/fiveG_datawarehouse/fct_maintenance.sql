SELECT
    maintenance_id,
    MD5(CAST(truck_id AS VARCHAR)) AS truck_key,
    CAST(STRFTIME(maintenance_date, '%Y%m%d') AS INT) AS date_key,
    maintenance_type,
    odometer_reading,
    labor_hours,
    labor_cost,
    parts_cost,
    total_cost,
    facility_location,
    downtime_hours,
    service_description
FROM {{ ref('stg_maintenance_records') }}