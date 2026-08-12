import os
import subprocess
import sys
from prefect import flow, task
import ingest_crypto

@task(name="Ingest Live Crypto API Data")
def task_ingest_crypto():
    """Fetches CoinGecko API data and loads into raw_crypto_markets."""
    data = ingest_crypto.fetch_live_crypto_data()
    ingest_crypto.load_to_landing_zone(data)

@task(name="Run & Test Data Vault Models")
def task_run_dbt():
    """Executes dbt transformations and runs assertions using standard CLI commands."""
    env = os.environ.copy()
    env["PYTHONWARNINGS"] = "ignore"

    # 1. Execute dbt run
    run_res = subprocess.run(
        ["dbt", "run", "--project-dir", "ecommerce_dv", "--profiles-dir", "ecommerce_dv"],
        capture_output=True,
        text=True,
        env=env,
    )
    if run_res.stdout:
        print(run_res.stdout)

    if run_res.returncode != 0:
        error_msg = run_res.stderr or run_res.stdout
        raise RuntimeError(f"dbt run failed:\n{error_msg}")

    # 2. Execute dbt test
    test_res = subprocess.run(
        ["dbt", "test", "--project-dir", "ecommerce_dv", "--profiles-dir", "ecommerce_dv"],
        capture_output=True,
        text=True,
        env=env,
    )
    if test_res.stdout:
        print(test_res.stdout)

    if test_res.returncode != 0:
        error_msg = test_res.stderr or test_res.stdout
        raise RuntimeError(f"dbt test failed:\n{error_msg}")

@flow(name="Cloud Crypto Data Vault Orchestrator")
def crypto_pipeline():
    task_ingest_crypto()
    task_run_dbt()

if __name__ == "__main__":
    # Runs the flow instantly in your terminal
    crypto_pipeline()