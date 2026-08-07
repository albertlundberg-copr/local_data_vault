{{ config(materialized='view') }}

WITH hub AS (
    SELECT 
        crypto_hk,
        coin_id
    FROM {{ ref('hub_crypto') }}
),

sat AS (
    SELECT 
        crypto_hk,
        load_date,
        current_price,
        market_cap,
        total_volume,
        ROW_NUMBER() OVER (PARTITION BY crypto_hk ORDER BY load_date DESC) as row_num
    FROM {{ ref('sat_crypto_market_metrics') }}
)

SELECT 
    h.coin_id,
    s.load_date AS last_updated_at,
    s.current_price,
    s.market_cap,
    s.total_volume
FROM hub h
INNER JOIN sat s 
    ON h.crypto_hk = s.crypto_hk
WHERE s.row_num = 1