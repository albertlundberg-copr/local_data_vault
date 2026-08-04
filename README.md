# Automated E-Commerce Data Vault & Info Mart Platform

An end-to-end, production-grade Modern Data Stack built with Python, DuckDB, dbt, AutomateDV, and Prefect, fully protected by GitHub Actions CI/CD.

## Architecture & Flow
1. **Ingestion Engine**: Custom Python script generating live transactional orders.
2. **Orchestrator**: Prefect flow managing ingestion and triggering dbt execution loops.
3. **Data Warehouse**: DuckDB storing landing, staging, vault, and mart layers.
4. **Data Vault 2.0 Layer**: Standardized staging, Hubs (Identity), Satellites (Context), and Links (Relationships) generated via AutomateDV.
5. **Information Mart**: Business-ready Star Schema (`dim_customers`, `fct_orders`) for analytics.
6. **CI/CD Quality Control**: GitHub Actions testing data integrity (`unique`, `not_null`, `relationships`) on every code push.

## How to Run Locally

1. Clone repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   cd ecommerce_dv && dbt deps && cd ..