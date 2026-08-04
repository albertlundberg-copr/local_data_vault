import os
import subprocess
import random
from datetime import datetime
import duckdb
from prefect import task, flow

# ==========================================
# DYNAMIC PATH RESOLUTION (Bulletproof Setup)
# ==========================================
# Get the absolute folder where THIS pipeline.py script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Smart check: Are we in the root folder or inside the subfolder?
if os.path.exists(os.path.join(SCRIPT_DIR, "ecommerce_dv")):
    # Script is in the root folder (local_data_vault/)
    DB_PATH = os.path.join(SCRIPT_DIR, "ecommerce_dv", "dev.duckdb")
    PROJECT_DIR = os.path.join(SCRIPT_DIR, "ecommerce_dv")
else:
    # Script is inside the subfolder (ecommerce_dv/)
    DB_PATH = os.path.join(SCRIPT_DIR, "dev.duckdb")
    PROJECT_DIR = SCRIPT_DIR

print(f"--- PATH CHECK ---")
print(f"Target Database: {DB_PATH}")
print(f"Target dbt Project: {PROJECT_DIR}")
print(f"------------------")

# ==========================================
# TASK 1: Live Mock Data Ingestion Engine
# ==========================================
@task(name="Extract & Load Live Orders")
def extract_and_load_orders():
    """Simulates an upstream app inserting new orders into the raw landing zone."""
    print(f"Connecting to landing database at: {DB_PATH}")
    
    conn = duckdb.connect(DB_PATH)
    
    # 1. Create the raw target table if it doesn't exist yet
    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_orders (
            order_id INTEGER,
            customer_id INTEGER,
            order_date TIMESTAMP,
            amount DECIMAL(10,2)
        )
    """)
    
    # 2. Generate a randomized order for our existing customers (1001, 1002, 1003)
    mock_order_id = random.randint(10000, 99999)
    mock_customer_id = random.choice([1001, 1002, 1003])
    mock_amount = round(random.uniform(15.50, 450.00), 2)
    current_time = datetime.now()
    
    # 3. Insert the record into the raw landing table
    conn.execute("""
        INSERT INTO raw_orders (order_id, customer_id, order_date, amount) 
        VALUES (?, ?, ?, ?)
    """, (mock_order_id, mock_customer_id, current_time, mock_amount))
    
    # Quick sanity check print to see the table size grow
    total_rows = conn.execute("SELECT COUNT(*) FROM raw_orders").fetchone()[0]
    print(f" Loaded Order #{mock_order_id} for Customer {mock_customer_id} (${mock_amount})")
    print(f" Total records sitting in raw_orders: {total_rows}")
    
    conn.close()

# ==========================================
# TASK 2: dbt Transformation Trigger
# ==========================================
@task(name="Trigger dbt Warehouse Transformation")
def run_dbt_pipeline():
    """Uses system shell execution to run the dbt transformation layer."""
    print("Initiating dbt compilation and execution loop...")
    
    # Execute 'dbt run' telling dbt to look in PROJECT_DIR for profiles.yml
    result = subprocess.run(
        ["dbt", "run", "--profiles-dir", PROJECT_DIR], 
        cwd=PROJECT_DIR, 
        capture_output=True, 
        text=True
    )
    
    # Print dbt's terminal output back into our orchestrator logs
    print(result.stdout)
    
    # If dbt fails, print stderr and raise an exception
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"dbt transformation execution failed!\n{result.stderr}")

# ==========================================
# THE CORE PIPELINE ORCHESTRATOR (THE FLOW)
# ==========================================
@flow(name="E-Commerce Data Vault Platform Pipeline")
def scheduled_vault_pipeline():
    # Step 1: Ingest live data into the raw staging area
    extract_and_load_orders()
    
    # Step 2: Trigger dbt to process the Data Vault models
    run_dbt_pipeline()

if __name__ == "__main__":
    import sys

    # If you explicitly pass '--serve' in terminal, run the continuous loop
    if "--serve" in sys.argv:
        print("Initializing continuous scheduler...")
        scheduled_vault_pipeline.serve(
            name="data-vault-continuous-loop",
            interval=60
        )
    # Default behavior: Run the pipeline ONCE and shut down cleanly
    else:
        print("Executing single pipeline run...")
        scheduled_vault_pipeline()