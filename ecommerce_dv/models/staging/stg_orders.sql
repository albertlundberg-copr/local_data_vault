{%- set yaml_metadata -%}
source_model:
  landing_zone: 'raw_orders'     # Changed from a string to a source-mapping dictionary
derived_columns:
  RECORD_SOURCE: '!LIVE_APP'
  LOAD_DATETIME: 'now()'
hashed_columns:
  ORDER_HK: 'order_id'
  CUSTOMER_HK: 'customer_id'
  LINK_CUSTOMER_ORDER_HK:
    - 'customer_id'
    - 'order_id'
  ORDER_HASHDIFF:
    - 'amount'
    - 'order_date'
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ automate_dv.stage(source_model=metadata_dict['source_model'],
                     derived_columns=metadata_dict['derived_columns'],
                     hashed_columns=metadata_dict['hashed_columns']) }}