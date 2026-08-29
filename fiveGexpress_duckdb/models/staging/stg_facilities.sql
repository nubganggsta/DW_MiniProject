WITH raw_data AS (
    SELECT 
        *,
        CURRENT_TIMESTAMP AS stg_loaded_at,
        'facilities.csv' AS source_filename,
        'BATCH_2026' AS batch_id
    FROM {{ source('fivegexpress', 'facilities') }}
),
cleansed AS (
    SELECT 
        UPPER(TRIM(CAST(facility_id AS VARCHAR))) AS facility_id,
        TRIM(CAST(facility_name AS VARCHAR)) AS facility_name,
        COALESCE(NULLIF(TRIM(CAST(city AS VARCHAR)), ''), 'Unknown') AS city,
        UPPER(COALESCE(NULLIF(TRIM(CAST(state AS VARCHAR)), ''), 'N/A')) AS state,
        TRY_CAST(latitude AS FLOAT) AS latitude,
        TRY_CAST(longitude AS FLOAT) AS longitude,
        COALESCE(TRY_CAST(dock_doors AS INT), 0) AS dock_doors,
        COALESCE(NULLIF(TRIM(CAST(operating_hours AS VARCHAR)), ''), 'Unspecified') AS operating_hours,
        stg_loaded_at,
        source_filename,
        batch_id
    FROM raw_data
),
validated AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY facility_id 
            ORDER BY stg_loaded_at
        ) AS dup_rank
    FROM cleansed
    WHERE facility_id IS NOT NULL
)
SELECT 
    facility_id,
    facility_name,
    city,
    state,
    latitude,
    longitude,
    dock_doors,
    operating_hours,
    stg_loaded_at,
    source_filename,
    batch_id
FROM validated
WHERE dup_rank = 1