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
DATA WAREHOUSE
      |
      v
DATA MARTS
```

Layer roles:
- **OLTP**: operational system for transactions.
- **Staging**: raw landing layer between source and analytics.
- **Data Warehouse**: dimensional model for analytics.
- **Data Marts**: aggregated views for reporting.

## Tech Stack

- Python
- SQL (PostgreSQL)
- Pandas
- Docker (optional)

## Data Model

Fact table:

```text
fact_sales
```

Dimension tables:

```text
dim_users
dim_products
```

## Pipeline Steps

1. **Extract**
   Load source data from CSV/mock source.

2. **Transform**
   Clean data, prepare dimensions, and build fact rows.

3. **Load**
   Load dimensions and fact table into PostgreSQL DWH.

## SQL Layer

- `sql/create_tables.sql`: OLTP tables (`users`, `products`, `orders`)
- `sql/dwh_schema.sql`: DWH tables (`dim_users`, `dim_products`, `fact_sales`) with surrogate keys
- `sql/marts.sql`: marts/views (`sales_by_product`, `sales_by_user`)

## How to Run

```bash
pip install -r requirements.txt
python src/pipeline.py --dry-run
python src/pipeline.py
```

Optional: set a custom connection string via `DATABASE_URL`.

## Interview Notes

Key concepts covered by this project:
- OLTP vs DWH
- staging layer purpose
- fact vs dimension tables
- ETL pipeline flow
