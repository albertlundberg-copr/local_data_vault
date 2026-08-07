import duckdb
import pandas as pd
import requests


def fetch_live_crypto_data():
    """Fetches top crypto market data from CoinGecko API and formats staging fields."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 5,
        "page": 1,
        "sparkline": "false",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    print("Fetching live market data from CoinGecko API...")

    df = pd.DataFrame(response.json())
    df["fetched_at"] = pd.Timestamp.now(tz="UTC")
    df["coin_id"] = df["id"]
    return df


def load_to_landing_zone(data):
    """Loads crypto DataFrame into MotherDuck landing table with dynamic schema sync."""
    with duckdb.connect("md:crypto_vault") as conn:
        conn.register("temp_crypto_data", data)

        conn.sql(
            "CREATE TABLE IF NOT EXISTS raw_crypto_markets AS SELECT * FROM"
            " temp_crypto_data WHERE 1=0;"
        )

        cols_count = conn.sql(
            "SELECT COUNT(*) FROM information_schema.columns WHERE table_name ="
            " 'raw_crypto_markets'"
        ).fetchone()[0]

        if cols_count != len(data.columns):
            conn.sql(
                "CREATE OR REPLACE TABLE raw_crypto_markets AS SELECT * FROM"
                " temp_crypto_data;"
            )
        else:
            conn.sql("""
                INSERT INTO raw_crypto_markets 
                SELECT * FROM temp_crypto_data 
                WHERE id NOT IN (SELECT id FROM raw_crypto_markets);
            """)

        total_rows = conn.sql(
            "SELECT COUNT(*) FROM raw_crypto_markets"
        ).fetchone()[0]
        print(f"Successfully ingested {len(data)} live crypto records.")
        print(f"Total rows sitting in raw_crypto_markets: {total_rows}")