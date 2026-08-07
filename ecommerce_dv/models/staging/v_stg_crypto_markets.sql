{%- set yaml_metadata -%}
source_model:
  main: 'raw_crypto_markets'
derived_columns:
  RECORD_SOURCE: "!COINGECKO_API"
  LOAD_DATE: "fetched_at"
hashed_columns:
  CRYPTO_HK: "coin_id"
  HASHDIFF:
    is_hashdiff: true
    columns:
      - "current_price"
      - "market_cap"
      - "total_volume"
      - "price_change_percentage_24h"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ automate_dv.stage(include_source_columns=true,
                     source_model=metadata_dict['source_model'],
                     derived_columns=metadata_dict['derived_columns'],
                     null_columns=none,
                     hashed_columns=metadata_dict['hashed_columns'],
                     ranked_columns=none) }}