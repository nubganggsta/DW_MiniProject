with stg_customers as (

    select * from {{ ref('stg_customers') }}

),

cleaned as (

    select
        -- Business Key
        trim(cast(customer_id as string)) as customer_id,

        -- Attributes
        trim(cast(customer_name as string)) as customer_name,
        coalesce(trim(cast(customer_type as string)), 'Individual') as customer_type,
        coalesce(cast(credit_terms_days as integer), 0) as credit_terms_days,
        coalesce(trim(cast(primary_freight_type as string)), 'Standard') as primary_freight_type,
        coalesce(trim(cast(account_status as string)), 'Active') as account_status,
        cast(contract_start_date as date) as contract_start_date,
        coalesce(cast(annual_revenue_potential as numeric), 0.00) as annual_revenue_potential,
        ingestion_timestamp

    from stg_customers
    where customer_id is not null 
      and trim(cast(customer_id as string)) <> ''

),

deduplicated as (

    select
        *,
        row_number() over (
            partition by customer_id
            order by contract_start_date desc, ingestion_timestamp desc
        ) as row_num

    from cleaned

),

final as (

    select
        -- Primary Key (Surrogate Key) Aligned with Diagram
        {{ dbt.generate_surrogate_key(['customer_id']) }} as customer_key,
        
        -- Diagram Attributes
        customer_id,
        customer_name,
        customer_type,
        credit_terms_days,
        primary_freight_type,
        account_status,
        contract_start_date,
        annual_revenue_potential

    from deduplicated
    where row_num = 1

)

select * from final