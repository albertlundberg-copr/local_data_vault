{%- set yaml_metadata -%}
source_model: 'raw_customers'
derived_columns:
  RECORD_SOURCE: '!CSV_CUSTOMERS'
  LOAD_DATETIME: 'now()'         # Changed from current_timestamp() to now()
hashed_columns:
  CUSTOMER_HK: 'customer_id'
  CUSTOMER_HASHDIFF:
    - 'first_name'
    - 'last_name'
    - 'email'
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ automate_dv.stage(source_model=metadata_dict['source_model'],
                     derived_columns=metadata_dict['derived_columns'],
                     hashed_columns=metadata_dict['hashed_columns']) }}