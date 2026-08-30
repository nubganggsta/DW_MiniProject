{{ config(
    materialized='table'
) }}

with customers as (

    select *
    from {{ ref('stg_customers') }}

)

select
    -- Primary Key (Surrogate Key)
    md5(cast(customer_id as {{ dbt.type_string() }})) as Customer_Key,

    -- Business Key & Attributes
    customer_id as Customer_ID,
    customer_name as Customer_Name,
    customer_type as Customer_Type,
    credit_terms_days as Payment_Terms,
    primary_freight_type as Primary_Freight,
    account_status as Status

from customers