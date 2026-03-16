[English](./README.md) | [Українська](./README.uk.md)

# Retail Data Pipeline & Data Warehouse

## Огляд Проєкту

Цей проєкт демонструє простий, але наближений до production data pipeline для retail-аналітики.
Він використовує layer архітектуру: **OLTP -> Staging -> DWH -> Data Marts**.
Бізнес-кейс — мережа роздрібних магазинів із даними про продажі.

## Архітектура

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

Ролі шарів:
- **OLTP**: операційна система для транзакцій.
- **Staging**: сирий проміжний layer між джерелом і аналітикою.
- **Data Warehouse**: вимірна fact-модель для аналітики.
- **Data Marts**: агреговані бізнес-вітрини для звітності.

## Технологічний Стек

- Python
- SQL (PostgreSQL + ClickHouse)
- Docker (опційно)

## Модель Даних

Основна DWH-таблиця:

```text
fact_sales
```

Таблиці вимірів:

```text
dim_users
dim_products
```

## Кроки Pipeline

1. **OLTP -> Staging**
   Інкрементальний UPSERT з `public` у `staging` за watermark.

2. **Staging -> DWH**
   Завантаження вимірів і інкрементальне додавання в `fact_sales`.

3. **DWH -> Marts**
   Оновлення вітрин: `sales_daily`, `sales_by_product`, `sales_by_city`, `sales_by_user`.

## SQL Шар

- `start_sql/create_tables.sql`: OLTP-таблиці + staging-дзеркало (`users`, `products`, `orders`, `order_items`)
- `start_sql/dwh_schema.sql`: DWH-таблиці в ClickHouse (`dim_users`, `dim_products`, `fact_sales`)
- `start_sql/marts.sql`: таблиці вітрин у ClickHouse (`sales_daily`, `sales_by_product`, `sales_by_city`, `sales_by_user`)

## Приклади Даних

Приклади зрізів по шарах знаходяться у:

```text
data_examples/OLTP
data_examples/staging
data_examples/OLAP
data_examples/marts
```

## Як Запустити (End-to-End)

1. Налаштуй `.env`:
   - найпростіше: скопіювати шаблон без змін
   - PowerShell:
   ```powershell
   Copy-Item .env.example .env
   ```
   - або Linux/macOS:
   ```bash
   cp .env.example .env
   ```

2. Запусти весь стек:
   ```bash
   docker compose up -d
   ```

3. Підключися до OLTP PostgreSQL у DBeaver (або будь-якому SQL-клієнті):
   - Host: `127.0.0.1`
   - Port: `54321`
   - Database: `sql_practice`
   - User: `postgres`
   - Password: `postgres`
   Примітка: ми використовуємо кастомний зовнішній порт `54321`, щоб не конфліктувати з локальним PostgreSQL на `5432`.

4. Підключися до ClickHouse:
   - Host: `127.0.0.1`
   - HTTP Port: `81234`
   - User: `admin`
   - Password: `adminpass`
   - Database: `dwh`

5. Перевір ініціалізацію баз:
   - У PostgreSQL мають існувати схеми `public`, `staging`, `etl`, а в `public` мають бути seed-дані.
   - У ClickHouse мають існувати бази `dwh` і `mart` з таблицями.
   Приклади перевірки:
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

6. Відкрий Airflow:
   - URL: `http://localhost:8090`
   - Login: `admin`
   - Password: `admin`
   Увімкни DAG `dwh_pipeline` і натисни `Trigger DAG`.

7. Після успішного run онови дані в клієнті БД і перевір наповнення:
   - `staging.*` (PostgreSQL)
   - `dwh.dim_users`, `dwh.dim_products`, `dwh.fact_sales` (ClickHouse)
   - `mart.sales_daily`, `mart.sales_by_product`, `mart.sales_by_city`, `mart.sales_by_user` (ClickHouse)
   Дані мають коректно протекти через усі шари.

Зупинка стека:
```bash
docker compose down
```

## Очікуваний Результат

Після успішного завершення `dwh_pipeline` в Airflow:
- усі три task (`raw_etl`, `dwh_etl`, `refresh_marts`) зелені
- дані присутні на шарах `staging`, `dwh` та `mart`

## Підсумки Реалізації

Що реалізовано:
- End-to-end data platform: `OLTP (PostgreSQL) -> staging -> DWH (ClickHouse) -> marts`.
- Інкрементальний ETL `public -> staging` через watermark (`updated_at`, `id`).
- Завантаження `staging -> DWH` + перевірки якості даних.
- Оновлення вітрин (`sales_daily`, `sales_by_product`, `sales_by_city`, `sales_by_user`).
- Оркестрація через Airflow DAG у Docker-оточенні.

Чому навчився:
- Проєктувати шари даних і розділяти відповідальність між ними.
- Працювати з двома СУБД одночасно (PostgreSQL і ClickHouse).
- Будувати відтворюваний запуск через `docker compose` і `.env`.
- Валідувати дані та відлагоджувати ETL-пайплайн за логами Airflow.

З якими проблемами працював:
- Конфлікт timezone (naive vs aware datetime) в інкрементальному завантаженні.
- Колізії локальних портів із контейнерними сервісами.
- Узгодження схем між SQL-ініціалізацією, ETL-кодом і прикладами даних.

