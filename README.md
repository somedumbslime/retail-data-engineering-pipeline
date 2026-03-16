[English](./README.md) | [Українська](./README.uk.md)

# Retail Data Pipeline & Data Warehouse

## Project Overview

This project demonstrates a simple but production-style data pipeline for retail analytics.
It follows a layered architecture: **OLTP -> Staging -> DWH -> Data Marts**.
The business case is a retail store network with sales data.

## Architecture

```text
OLTP (PostgreSQL)
      |
      v
STAGING
      |
      v
DATA WAREHOUSE (ClickHouse)
      |
      v
DATA MARTS (ClickHouse)
```

Layer roles:
- **OLTP**: operational system for transactions.
- **Staging**: raw landing layer between source and analytics.
- **Data Warehouse**: dimensional fact model for analytics.
- **Data Marts**: aggregated business views for reporting.

## Tech Stack

- Python
- SQL (PostgreSQL + ClickHouse)
- Docker (optional)

## Data Model

Core DWH table:

```text
fact_sales
```

Dimension tables:

```text
dim_users
dim_products
```

## Pipeline Steps

1. **OLTP -> Staging**
   Incremental UPSERT from `public` to `staging` by watermark.

2. **Staging -> DWH**
   Load dimensions and incrementally append to `fact_sales`.

3. **DWH -> Marts**
   Refresh marts: `sales_daily`, `sales_by_product`, `sales_by_city`, `sales_by_user`.

## SQL Layer

- `start_sql/create_tables.sql`: OLTP tables + staging mirror (`users`, `products`, `orders`, `order_items`)
- `start_sql/dwh_schema.sql`: DWH tables in ClickHouse (`dim_users`, `dim_products`, `fact_sales`)
- `start_sql/marts.sql`: mart tables in ClickHouse (`sales_daily`, `sales_by_product`, `sales_by_city`, `sales_by_user`)

## Data Examples

Example snapshots by layer are in:

```text
data_examples/OLTP
data_examples/staging
data_examples/OLAP
data_examples/marts
```

## How to Run (End-to-End)

1. Configure `.env`:
   - easiest option: copy template as-is
   - PowerShell:
   ```powershell
   Copy-Item .env.example .env
   ```
   - Linux/macOS:
   ```bash
   cp .env.example .env
   ```

2. Start the full stack:
   ```bash
   docker compose up -d
   ```

3. Connect to OLTP PostgreSQL in DBeaver (or any SQL client):
   - Host: `127.0.0.1`
   - Port: `54321`
   - Database: `sql_practice`
   - User: `postgres`
   - Password: `postgres`
   Note: we use custom external port `54321` to avoid conflicts with a local PostgreSQL on `5432`.

4. Connect to ClickHouse:
   - Host: `127.0.0.1`
   - HTTP Port: `81234`
   - User: `admin`
   - Password: `adminpass`
   - Database: `dwh`

5. Verify database bootstrap:
   - PostgreSQL should contain schemas `public`, `staging`, `etl`, and `public` should have seed rows.
   - ClickHouse should contain `dwh` and `mart` databases with tables.
   Example checks:
   ```sql
   -- PostgreSQL
   SELECT table_schema, table_name
   FROM information_schema.tables
   WHERE table_schema IN ('public', 'staging', 'etl')
   ORDER BY 1, 2;

   SELECT COUNT(*) AS oltp_orders FROM public.orders;
   ```
   ```sql
   -- ClickHouse
   SHOW DATABASES;
   SHOW TABLES FROM dwh;
   SHOW TABLES FROM mart;
   ```

6. Open Airflow:
   - URL: `http://localhost:8090`
   - Login: `admin`
   - Password: `admin`
   Enable DAG `dwh_pipeline` and click `Trigger DAG`.

7. After a successful run, refresh DB client views and validate data flow:
   - `staging.*` (PostgreSQL)
   - `dwh.dim_users`, `dwh.dim_products`, `dwh.fact_sales` (ClickHouse)
   - `mart.sales_daily`, `mart.sales_by_product`, `mart.sales_by_city`, `mart.sales_by_user` (ClickHouse)
   Data should flow correctly through all layers.

Stop stack:
```bash
docker compose down
```

## Expected Result

After `dwh_pipeline` finishes successfully in Airflow:
- all three tasks (`raw_etl`, `dwh_etl`, `refresh_marts`) are green
- data is available in `staging`, `dwh`, and `mart` layers

Screenshot placeholders (replace with your own):

![Airflow DAG Success](docs/screenshots/airflow_dag_success.png)
![DWH and Marts Data Check](docs/screenshots/dwh_marts_data_check.png)

## Project Outcomes

Implemented:
- End-to-end data platform: `OLTP (PostgreSQL) -> staging -> DWH (ClickHouse) -> marts`.
- Incremental ETL for `public -> staging` using watermark (`updated_at`, `id`).
- `staging -> DWH` loading with data quality checks.
- Mart refresh for `sales_daily`, `sales_by_product`, `sales_by_city`, `sales_by_user`.
- Airflow DAG orchestration in a Docker-based environment.

Learned:
- How to design layered data architecture and separate responsibilities by layer.
- How to work with PostgreSQL and ClickHouse in one pipeline.
- How to make a reproducible local stack with `docker compose` and `.env`.
- How to troubleshoot ETL failures from Airflow logs and SQL checks.

Challenges solved:
- Timezone mismatch (naive vs aware datetime) in incremental loads.
- Container port conflicts with local DB services.
- Schema alignment across SQL bootstrap scripts, ETL code, and sample data.


