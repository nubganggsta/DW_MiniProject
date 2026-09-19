with stg_customers as (

    select *
    from {{ ref('stg_customers') }}

),

cleaned as (

    select
        -- Business Key
        trim(cast(customer_id as string)) as cleaned_customer_id,

        -- Attributes
        trim(cast(customer_name as string)) as customer_name,
        trim(cast(customer_type as string)) as customer_type,
        cast(credit_terms_days as integer) as credit_terms_days,
        trim(cast(primary_freight_type as string)) as primary_freight_type,
        trim(cast(account_status as string)) as account_status,
        
        -- Date Parsing
        cast(contract_start_date as date) as contract_start_date,
        cast(annual_revenue_potential as numeric(15,2)) as annual_revenue_potential,
        ingestion_timestamp

    from stg_customers
    where customer_id is not null 
      and trim(cast(customer_id as string)) <> ''

),

deduplicated as (

    select
        *,
        row_number() over (
            partition by cleaned_customer_id
            order by contract_start_date desc, ingestion_timestamp desc
        ) as row_num

    from cleaned

),

final as (

    select
        -- Surrogate Key ตรงตาม ER Diagram
        {{ dbt_utils.generate_surrogate_key(['cleaned_customer_id']) }} as customer_key,
        
        -- Dimension Attributes (snake_case)
        cleaned_customer_id as customer_id,
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

select *
from final