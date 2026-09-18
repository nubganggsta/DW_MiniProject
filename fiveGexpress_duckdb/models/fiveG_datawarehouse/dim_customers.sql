-- ============================================================================
-- Script: Dim_Customer Dimension Table Creation & ETL Script
-- Dialect: Standard ANSI SQL (Compatible with PostgreSQL, Snowflake, BigQuery)
-- Description: DDL, Cleansing, Transformation, and Quality Validation for Dim_Customer
-- ============================================================================

-- 1. CREATE DIMENSION TABLE (DDL)
DROP TABLE IF EXISTS Dim_Customer;

CREATE TABLE Dim_Customer (
    Customer_SK              INT NOT NULL PRIMARY KEY,            -- Surrogate Key (Primary Key for DWH)
    Customer_ID              VARCHAR(50) NOT NULL UNIQUE,          -- Business Key / Natural Key from Source
    Customer_Name            VARCHAR(255) NOT NULL,               -- Customer / Company Name
    Customer_Type            VARCHAR(50),                         -- Customer Category (Corporate, SME, Individual, Enterprise)
    Credit_Terms_Days        INT,                                 -- Payment Credit Terms in Days
    Primary_Freight_Type     VARCHAR(50),                         -- Main Transport Mode (Express Air, Freight Land, etc.)
    Account_Status           VARCHAR(20) DEFAULT 'Active',        -- Account Status (Active, Inactive, Suspended)
    Contract_Start_Date      DATE,                                -- Contract Start Date (YYYY-MM-DD)
    Annual_Revenue_Potential DECIMAL(15, 2) DEFAULT 0.00          -- Estimated Annual Revenue (THB)
);

-- 2. ETL/ELT TRANSFORMATION & INSERTION PIPELINE
-- CTE to clean, cast, deduplicate, and assign Surrogate Keys
WITH stg_customers AS (
    SELECT
        -- Business Key Cleanup
        TRIM(CAST(customer_id AS VARCHAR(50))) AS cleaned_customer_id,
        
        -- Text Attributes Cleanup
        TRIM(CAST(customer_name AS VARCHAR(255))) AS cleaned_customer_name,
        COALESCE(TRIM(CAST(customer_type AS VARCHAR(50))), 'Individual') AS cleaned_customer_type,
        
        -- Numeric Parsing & Safe Casting
        COALESCE(CAST(credit_terms_days AS INT), 0) AS cleaned_credit_terms,
        COALESCE(TRIM(CAST(primary_freight_type AS VARCHAR(50))), 'Standard') AS cleaned_freight_type,
        COALESCE(TRIM(CAST(account_status AS VARCHAR(20))), 'Active') AS cleaned_account_status,
        
        -- Date Casting (Standard YYYY-MM-DD format)
        CAST(contract_start_date AS DATE) AS cleaned_contract_start_date,
        
        -- Financial Metric Casting
        COALESCE(CAST(annual_revenue_potential AS DECIMAL(15,2)), 0.00) AS cleaned_annual_revenue
    FROM raw_customers_stg
    WHERE customer_id IS NOT NULL 
      AND TRIM(customer_id) <> ''
),

deduplicated AS (
    SELECT
        cleaned_customer_id,
        cleaned_customer_name,
        cleaned_customer_type,
        cleaned_credit_terms,
        cleaned_freight_type,
        cleaned_account_status,
        cleaned_contract_start_date,
        cleaned_annual_revenue,
        -- Deduplication logic: Keep latest updated entry if duplicates exist
        ROW_NUMBER() OVER (
            PARTITION BY cleaned_customer_id 
            ORDER BY cleaned_contract_start_date DESC
        ) AS row_num
    FROM stg_customers
),

transformed_with_sk AS (
    SELECT
        -- Generate 1, 2, 3... Surrogate Key sequence ordered by Customer_ID
        ROW_NUMBER() OVER (ORDER BY cleaned_customer_id ASC) AS Customer_SK,
        cleaned_customer_id AS Customer_ID,
        cleaned_customer_name AS Customer_Name,
        cleaned_customer_type AS Customer_Type,
        cleaned_credit_terms AS Credit_Terms_Days,
        cleaned_freight_type AS Primary_Freight_Type,
        cleaned_account_status AS Account_Status,
        cleaned_contract_start_date AS Contract_Start_Date,
        cleaned_annual_revenue AS Annual_Revenue_Potential
    FROM deduplicated
    WHERE row_num = 1
)

INSERT INTO Dim_Customer (
    Customer_SK,
    Customer_ID,
    Customer_Name,
    Customer_Type,
    Credit_Terms_Days,
    Primary_Freight_Type,
    Account_Status,
    Contract_Start_Date,
    Annual_Revenue_Potential
)
SELECT 
    Customer_SK,
    Customer_ID,
    Customer_Name,
    Customer_Type,
    Credit_Terms_Days,
    Primary_Freight_Type,
    Account_Status,
    Contract_Start_Date,
    Annual_Revenue_Potential
FROM transformed_with_sk;

-- 3. DATA QUALITY & INTEGRITY CHECK SUITE

-- Check 1: Duplicate Surrogate Key Check (Must return 0)
SELECT 
    'Duplicate SK Check' AS test_name,
    COUNT(Customer_SK) - COUNT(DISTINCT Customer_SK) AS failed_records
FROM Dim_Customer;

-- Check 2: Duplicate Business Key Check (Must return 0)
SELECT 
    'Duplicate Business Key Check' AS test_name,
    COUNT(Customer_ID) - COUNT(DISTINCT Customer_ID) AS failed_records
FROM Dim_Customer;

-- Check 3: NULL Value Checks on Required Columns (Must return 0)
SELECT 
    'Mandatory NULL Check' AS test_name,
    COUNT(*) AS null_records_count
FROM Dim_Customer
WHERE Customer_SK IS NULL 
   OR Customer_ID IS NULL 
   OR Customer_Name IS NULL;

-- Check 4: Data Profiling Verification
SELECT 
    COUNT(*) AS total_rows,
    COUNT(DISTINCT Customer_SK) AS unique_sks,
    COUNT(DISTINCT Customer_ID) AS unique_customer_ids,
    MIN(Contract_Start_Date) AS earliest_contract,
    MAX(Contract_Start_Date) AS latest_contract,
    SUM(Annual_Revenue_Potential) AS total_revenue_potential
FROM Dim_Customer;