{%- set yaml_metadata -%}
src_pk: "CRYPTO_HK"
src_nk: "coin_id"
src_ldts: "LOAD_DATE"
src_source: "RECORD_SOURCE"
source_model: "v_stg_crypto_markets"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ automate_dv.hub(src_pk=metadata_dict['src_pk'],
                   src_nk=metadata_dict['src_nk'],
                   src_ldts=metadata_dict['src_ldts'],
                   src_source=metadata_dict['src_source'],
                   source_model=metadata_dict['source_model']) }}