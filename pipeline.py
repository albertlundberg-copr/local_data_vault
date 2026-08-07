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
    """Executes dbt transformations and runs assertions in an isolated process."""
    runner_code = (
        "from dbt.cli.main import dbtRunner; "
        "runner = dbtRunner(); "
        "res_run = runner.invoke(['run', '--project-dir', 'ecommerce_dv', '--profiles-dir', 'ecommerce_dv']); "
        "if not res_run.success: exit(1); "
        "res_test = runner.invoke(['test', '--project-dir', 'ecommerce_dv', '--profiles-dir', 'ecommerce_dv']); "
        "exit(0 if res_test.success else 1)"
    )

    env = os.environ.copy()
    env["PYTHONWARNINGS"] = "ignore"

    result = subprocess.run(
        [sys.executable, "-c", runner_code],
        capture_output=True,
        text=True,
        env=env,
    )

    if result.stdout:
        print(result.stdout)

    if result.returncode != 0:
        error_details = result.stdout.strip() or result.stderr.strip() or "Unknown dbt error"
        raise RuntimeError(f"dbt run/test failed:\n{error_details}")


@flow(name="Cloud Crypto Data Vault Orchestrator")
def crypto_pipeline():
    task_ingest_crypto()
    task_run_dbt()


if __name__ == "__main__":
    # Replaced manual execution with an automated schedule
    crypto_pipeline.serve(
        name="crypto-vault-ingestion-deployment",
        cron="*/15 * * * *",  # Runs every 15 minutes
        tags=["crypto", "motherduck", "dbt"]
    )