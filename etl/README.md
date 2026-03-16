[English](./README.md) | [Українська](./README.uk.md)

# ETL Folder Layout

## Main entry scripts

- `python -m pipelines.oltp_to_staging` -> pipeline **OLTP -> Staging**
- `python -m pipelines.staging_to_dwh` -> pipeline **Staging -> DWH**
- `python -m pipelines.marts_refresh` -> pipeline **DWH -> Data Marts**

These three files are lightweight entrypoints. Main logic is in subfolders below.

## Internal structure

- `pipelines/`
  - `oltp_to_staging.py` - incremental UPSERT from `public` to `staging`
  - `staging_to_dwh.py` - load `dim_*` and incremental `fact_sales` + DQ checks
  - `marts_refresh.py` - refresh marts from DWH (`sales_daily`, `sales_by_product`, `sales_by_city`, `sales_by_user`)
- `core/`
  - shared config, logging, Postgres and ClickHouse clients
- `dwh/`
  - DWH loaders, SQL transforms, watermark utilities, data quality checks
- `marts_layer/`
  - SQL for marts refresh

## Run commands

```bash
cd etl
python -m pipelines.oltp_to_staging
python -m pipelines.staging_to_dwh
python -m pipelines.marts_refresh
```

## Environment Variables

ETL clients read these vars:
- `APP_POSTGRES_HOST`, `APP_POSTGRES_DB`, `APP_POSTGRES_USER`, `APP_POSTGRES_PASSWORD`, `APP_POSTGRES_PORT`
- `APP_CLICKHOUSE_HOST`, `APP_CLICKHOUSE_PORT`, `APP_CLICKHOUSE_USER`, `APP_CLICKHOUSE_PASSWORD`, `APP_CLICKHOUSE_DB`

You can define them in:
- project root: `.env`
- or `etl/.env`

If `python-dotenv` is not installed, set variables in shell or Docker/Airflow environment.

