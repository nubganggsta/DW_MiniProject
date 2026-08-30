{{ config(
    materialized='table'
) }}

with customers as (

    select *
    from {{ ref('stg_customers') }}

)
 
select
    -- Primary Key (Surrogate Key)
    md5(cast(customer_id as {{ dbt.type_string() }})) as customer_key,

    -- Business Key & Attributes
    customer_id as customer_id,
    customer_name as customer_name,
    customer_type as customer_type,
    credit_terms_days as payment_terms,
    primary_freight_type as primary_freight,
    account_status as Status

from customers