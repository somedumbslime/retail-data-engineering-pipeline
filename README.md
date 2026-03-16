[English](./README.md) | [Українська](./README.uk.md)

# Retail Data Pipeline & Data Warehouse

A production-style data pipeline for retail analytics demonstrating layered data architecture, incremental ETL, and Airflow orchestration.

The project simulates a retail store network and implements a full data flow from transactional systems to analytical data marts.

---

# Project Overview

This project demonstrates how a modern data platform can be structured using a layered architecture:

`OLTP -> Staging -> Data Warehouse -> Data Marts`

The pipeline processes retail sales data and prepares it for analytical queries and reporting.

The implementation focuses on:

- layered data architecture
- incremental ETL pipelines
- dimensional modeling (fact + dimension tables)
- orchestration with Airflow
- reproducible environment with Docker

---

# Architecture

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

## Layer Responsibilities

### OLTP
Operational transactional database storing raw business events.

### Staging
Landing layer used to isolate source systems and prepare data for transformation.

### Data Warehouse
Dimensional analytical storage optimized for queries.

### Data Marts
Aggregated business views used for reporting and analytics.

---

# Tech Stack

## Languages
- Python
- SQL

## Databases
- PostgreSQL (OLTP + staging)
- ClickHouse (DWH + marts)

## Orchestration
- Airflow

## Infrastructure
- Docker

---

# Data Model

The warehouse follows a dimensional modeling approach.

## Fact Table

```text
fact_sales
```

Contains sales transactions enriched with dimensional references.

## Dimension Tables

```text
dim_users
dim_products
```

Provide descriptive attributes used for analytical slicing.

---

# Pipeline Flow

The data pipeline consists of three logical stages.

## 1. OLTP -> Staging

Incremental synchronization from the operational database.

Key characteristics:
- watermark-based incremental loading
- UPSERT logic
- source isolation

---

## 2. Staging -> Data Warehouse

Transformation and loading into dimensional schema.

Key steps:
- dimension loading
- fact table population
- data validation checks

---

## 3. Data Warehouse -> Data Marts

Aggregation layer for analytical queries.

Implemented marts:

```text
sales_daily
sales_by_product
sales_by_city
sales_by_user
```

---

# Project Structure

```text
retail-data-engineering-pipeline
|
|-- airflow
|   `-- dags
|
|-- etl
|   |-- core
|   |-- dwh
|   |-- marts_layer
|   `-- pipelines
|
|-- sql
|   |-- create_tables.sql
|   |-- dwh_schema.sql
|   |-- postgres_etl_metadata.sql
|   |-- seed_oltp.sql
|   `-- marts.sql
|
|-- data_examples
|   |-- OLTP
|   |-- staging
|   |-- OLAP
|   `-- marts
|
|-- docs
|
|-- docker-compose.yml
|-- requirements.txt
`-- README.md
```

---

# How to Run

## 1. Configure Environment

PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

## 2. Start Services

```bash
docker compose up -d
```

## 3. Connect to PostgreSQL

- Host: `127.0.0.1`
- Port: `54321`
- Database: `sql_practice`
- User: `postgres`
- Password: `postgres`

Custom external port `54321` avoids conflicts with local PostgreSQL on `5432`.

## 4. Connect to ClickHouse

- Host: `127.0.0.1`
- HTTP Port: `81234`
- User: `admin`
- Password: `adminpass`
- Database: `dwh`

## 5. Open Airflow

- URL: `http://localhost:8090`
- Login: `admin`
- Password: `admin`

Enable DAG `dwh_pipeline` and trigger it.

---

# Expected Result

After successful pipeline execution, all Airflow tasks:

```text
raw_etl
dwh_etl
refresh_marts
```

are completed successfully.

Data becomes available in:

## PostgreSQL

```text
staging.*
```

## ClickHouse

```text
dwh.dim_users
dwh.dim_products
dwh.fact_sales

mart.sales_daily
mart.sales_by_product
mart.sales_by_city
mart.sales_by_user
```

---

# Key Engineering Decisions

## PostgreSQL for OLTP
Chosen as a simple transactional database for simulating retail operations.

## ClickHouse for Analytics
Optimized for analytical workloads and large aggregations.

## Staging Layer
Decouples source schema from analytical transformations.

## Incremental Loading
Watermark-based approach prevents full reloads and reduces processing time.

## Airflow Orchestration
Provides visibility into pipeline execution and task dependencies.

---

# What I Learned

During this project I explored:

- layered data platform architecture
- dimensional modeling for analytics
- incremental ETL design
- orchestration with Airflow
- building reproducible local environments using Docker

---

# Challenges Solved

- timezone mismatch in incremental loads
- container port conflicts with local services
- schema alignment across SQL bootstrap scripts and ETL code

---

# Example Data

Example snapshots of each layer are available in:

```text
data_examples/
```

These examples illustrate how data evolves from OLTP records to analytical marts.
