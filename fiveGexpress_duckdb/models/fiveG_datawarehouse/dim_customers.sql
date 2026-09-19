{{ config(materialized='table') }}

WITH source AS (
    SELECT
        customer_id,
        customer_name,
        customer_type,
        credit_terms_days,
        primary_freight_type,
        account_status,
        CAST(
            COALESCE(
                TRY_STRPTIME(CAST(contract_start_date AS VARCHAR), '%m/%d/%Y %H:%M:%S'),
                TRY_STRPTIME(CAST(contract_start_date AS VARCHAR), '%Y-%m-%d'),
                TRY_STRPTIME(CAST(contract_start_date AS VARCHAR), '%m/%d/%Y')
            ) AS DATE
        ) AS contract_start_date,
        annual_revenue_potential,
        current_localtimestamp() AS insertion_timestamp
    FROM {{ ref('stg_customers') }}
),

unique_source AS (
    SELECT *,
            ROW_NUMBER() OVER (PARTITION BY customer_id) AS row_num
    FROM source
)

SELECT 
    ROW_NUMBER() OVER (ORDER BY customer_id) AS customer_key,
    * EXCLUDE (row_num)
FROM unique_source
WHERE row_num = 1