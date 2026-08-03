{%- set yaml_metadata -%}
source_model: 'stg_customers'
src_pk: 'CUSTOMER_HK'
src_hashdiff: 'CUSTOMER_HASHDIFF'
src_payload:
  - 'first_name'
  - 'last_name'
  - 'email'
src_ldts: 'LOAD_DATETIME'
src_source: 'RECORD_SOURCE'
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ automate_dv.sat(src_pk=metadata_dict['src_pk'],
                   src_hashdiff=metadata_dict['src_hashdiff'],
                   src_payload=metadata_dict['src_payload'],
                   src_ldts=metadata_dict['src_ldts'],
                   src_source=metadata_dict['src_source'],
                   source_model=metadata_dict['source_model']) }}