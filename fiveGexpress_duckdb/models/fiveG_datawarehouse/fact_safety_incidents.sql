SELECT
    MD5(CAST(incident_id AS VARCHAR)) AS safety_incident_key,
    incident_id,
    trip_id AS trip_id_degenerate_key,
    CAST(STRFTIME(incident_date, '%Y%m%d') AS INT) AS date_key,
    MD5(CAST(truck_id AS VARCHAR)) AS truck_key,
    MD5(CAST(driver_id AS VARCHAR)) AS driver_key,
    incident_type,
    1 AS incident_count,
    at_fault_flag AS at_fault,
    injury_flag AS injury,
    (COALESCE(vehicle_damage_cost, 0) + COALESCE(cargo_damage_cost, 0) + COALESCE(claim_amount, 0)) AS incident_cost
FROM {{ ref('stg_safety_incidents') }}