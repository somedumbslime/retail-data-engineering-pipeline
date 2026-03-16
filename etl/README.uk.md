[English](./README.md) | [Українська](./README.uk.md)

# Структура Папки ETL

## Основні entrypoint-скрипти

- `python -m pipelines.oltp_to_staging` -> pipeline **OLTP -> Staging**
- `python -m pipelines.staging_to_dwh` -> pipeline **Staging -> DWH**
- `python -m pipelines.marts_refresh` -> pipeline **DWH -> Data Marts**

Ці три файли — легкі точки входу. Основна логіка винесена в підпапки нижче.

## Внутрішня структура

- `pipelines/`
  - `oltp_to_staging.py` - інкрементальний UPSERT з `public` у `staging`
  - `staging_to_dwh.py` - завантаження `dim_*` і інкрементального `fact_sales` + DQ-перевірки
  - `marts_refresh.py` - оновлення вітрин із DWH (`sales_daily`, `sales_by_product`, `sales_by_city`, `sales_by_user`)
- `core/`
  - спільний конфіг, логування, клієнти Postgres і ClickHouse
- `dwh/`
  - DWH-завантажувачі, SQL-трансформації, watermark-утиліти, перевірки якості даних
- `marts_layer/`
  - SQL для оновлення вітрин

## Команди запуску

```bash
cd etl
python -m pipelines.oltp_to_staging
python -m pipelines.staging_to_dwh
python -m pipelines.marts_refresh
```

## Змінні Середовища

ETL-клієнти читають такі змінні:
- `APP_POSTGRES_HOST`, `APP_POSTGRES_DB`, `APP_POSTGRES_USER`, `APP_POSTGRES_PASSWORD`, `APP_POSTGRES_PORT`
- `APP_CLICKHOUSE_HOST`, `APP_CLICKHOUSE_PORT`, `APP_CLICKHOUSE_USER`, `APP_CLICKHOUSE_PASSWORD`, `APP_CLICKHOUSE_DB`

Їх можна задавати у:
- корені проєкту: `.env`
- або `etl/.env`

Якщо `python-dotenv` не встановлений, задавай змінні в shell або через Docker/Airflow environment.

