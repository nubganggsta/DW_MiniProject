WITH raw_data AS (
    SELECT
        *,
        CURRENT_TIMESTAMP AS stg_loaded_at,
        'trailers.csv' AS source_filename,
        'BATCH_2026' AS batch_id
    FROM {{ source('fivegexpress', 'trailers') }}
),

cleansed AS (
    SELECT
        UPPER(TRIM(CAST(trailer_id AS VARCHAR))) AS trailer_id,
        TRY_CAST(trailer_number AS INT) AS trailer_number,
        COALESCE(NULLIF(TRIM(CAST(trailer_type AS VARCHAR)), ''), 'Unspecified') AS trailer_type,
        TRY_CAST(length_feet AS INT) AS length_feet,
        TRY_CAST(model_year AS INT) AS model_year,
        UPPER(TRIM(CAST(vin AS VARCHAR))) AS vin,
        TRY_CAST(acquisition_date AS DATE) AS acquisition_date,
        COALESCE(NULLIF(TRIM(CAST(status AS VARCHAR)), ''), 'Unknown') AS status,
        COALESCE(NULLIF(TRIM(CAST(current_location AS VARCHAR)), ''), 'Unknown') AS current_location,
        stg_loaded_at,
        source_filename,
        batch_id
    FROM raw_data
),

validated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY trailer_id
            ORDER BY stg_loaded_at DESC
        ) AS dup_rank
    FROM cleansed
    WHERE trailer_id IS NOT NULL
)

SELECT
    trailer_id,
    trailer_number,
    trailer_type,
    length_feet,
    model_year,
    vin,
    acquisition_date,
    status,
    current_location,
    stg_loaded_at,
    source_filename,
    batch_id
FROM validated
WHERE dup_rank = 1