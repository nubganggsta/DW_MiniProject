WITH raw_data AS (
    SELECT
        *,
        CURRENT_TIMESTAMP AS stg_loaded_at,
        'customers.csv' AS source_filename,
        'BATCH_2026' AS batch_id
    FROM {{ source('fivegexpress', 'customers') }}
),

cleansed AS (
    SELECT
        UPPER(TRIM(CAST(customer_id AS VARCHAR))) AS customer_id,
        TRIM(CAST(customer_name AS VARCHAR)) AS customer_name,
        COALESCE(NULLIF(TRIM(CAST(customer_type AS VARCHAR)), ''), 'Unspecified') AS customer_type,
        COALESCE(TRY_CAST(credit_terms_days AS INT), 0) AS credit_terms_days,
        COALESCE(NULLIF(TRIM(CAST(primary_freight_type AS VARCHAR)), ''), 'General') AS primary_freight_type,
        COALESCE(NULLIF(TRIM(CAST(account_status AS VARCHAR)), ''), 'Unknown') AS account_status,
        TRY_CAST(contract_start_date AS DATE) AS contract_start_date,
        COALESCE(TRY_CAST(annual_revenue_potential AS DECIMAL(15,2)), 0.00) AS annual_revenue_potential,
        stg_loaded_at,
        source_filename,
        batch_id
    FROM raw_data
),

validated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY stg_loaded_at DESC
        ) AS dup_rank
    FROM cleansed
    WHERE customer_id IS NOT NULL
)

SELECT
    customer_id,
    customer_name,
    customer_type,
    credit_terms_days,
    primary_freight_type,
    account_status,
    contract_start_date,
    annual_revenue_potential,
    stg_loaded_at,
    source_filename,
    batch_id
FROM validated
WHERE dup_rank = 1