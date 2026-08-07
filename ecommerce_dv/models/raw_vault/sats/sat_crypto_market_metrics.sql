{%- set yaml_metadata -%}
src_pk: "CRYPTO_HK"
src_hashdiff: "HASHDIFF"
src_payload:
  - "symbol"
  - "name"
  - "current_price"
  - "market_cap"
  - "total_volume"
  - "price_change_percentage_24h"
src_ldts: "LOAD_DATE"
src_source: "RECORD_SOURCE"
source_model: "v_stg_crypto_markets"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ automate_dv.sat(src_pk=metadata_dict['src_pk'],
                   src_hashdiff=metadata_dict['src_hashdiff'],
                   src_payload=metadata_dict['src_payload'],
                   src_ldts=metadata_dict['src_ldts'],
                   src_source=metadata_dict['src_source'],
                   source_model=metadata_dict['source_model']) }}