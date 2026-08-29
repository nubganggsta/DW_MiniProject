WITH raw_data AS (
    SELECT
        *,
        CURRENT_TIMESTAMP AS stg_loaded_at,
        'safety_incidents.csv' AS source_filename,
        'BATCH_2026' AS batch_id
    FROM {{ source('fivegexpress', 'safety_incidents') }}
),
cleansed AS (
    SELECT
        UPPER(TRIM(CAST(incident_id AS VARCHAR))) AS incident_id,
        UPPER(TRIM(CAST(driver_id AS VARCHAR))) AS driver_id,
        UPPER(TRIM(CAST(trip_id AS VARCHAR))) AS trip_id,
        UPPER(TRIM(CAST(truck_id AS VARCHAR))) AS truck_id,
        TRY_CAST(incident_date AS TIMESTAMP) AS incident_date,
        COALESCE(NULLIF(TRIM(CAST(incident_type AS VARCHAR)), ''), 'Unspecified') AS incident_type,
        COALESCE(NULLIF(TRIM(CAST(location_city AS VARCHAR)), ''), 'Unknown') AS location_city,
        UPPER(COALESCE(NULLIF(TRIM(CAST(location_state AS VARCHAR)), ''), 'N/A')) AS location_state,
        COALESCE(TRY_CAST(at_fault_flag AS BOOLEAN), FALSE) AS at_fault_flag,
        COALESCE(TRY_CAST(injury_flag AS BOOLEAN), FALSE) AS injury_flag,
        COALESCE(TRY_CAST(vehicle_damage_cost AS DECIMAL(12,2)), 0.00) AS vehicle_damage_cost,
        COALESCE(TRY_CAST(cargo_damage_cost AS DECIMAL(12,2)), 0.00) AS cargo_damage_cost,
        COALESCE(TRY_CAST(claim_amount AS DECIMAL(12,2)), 0.00) AS claim_amount,
        COALESCE(TRY_CAST(preventable_flag AS BOOLEAN), FALSE) AS preventable_flag,
        TRIM(COALESCE(CAST(description AS VARCHAR), '')) AS description,
        stg_loaded_at,
        source_filename,
        batch_id
    FROM raw_data
),
validated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY incident_id
            ORDER BY stg_loaded_at
        ) AS dup_rank
    FROM cleansed
    WHERE incident_id IS NOT NULL
)
SELECT
    incident_id,
    driver_id,
    trip_id,
    truck_id,
    incident_date,
    incident_type,
    location_city,
    location_state,
    at_fault_flag,
    injury_flag,
    vehicle_damage_cost,
    cargo_damage_cost,
    claim_amount,
    preventable_flag,
    description,
    stg_loaded_at,
    source_filename,
    batch_id
FROM validated
WHERE dup_rank = 1
