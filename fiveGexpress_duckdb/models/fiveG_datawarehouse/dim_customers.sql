with customers as (

    select *
    from {{ ref('stg_customers') }}

)

select
    customer_id,
    customer_name,
    customer_type,
    credit_terms_days,
    primary_freight_type,
    account_status,
    contract_start_date,
    annual_revenue_potential,
    stg_loaded_at as dim_created_at

from customers