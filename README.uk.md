[English](./README.md) | [Українська](./README.uk.md)

# Retail Data Pipeline & Data Warehouse

Production-style data pipeline для retail-аналітики, що демонструє пошарову архітектуру даних, інкрементальний ETL і оркестрацію через Airflow.

Проєкт імітує мережу роздрібних магазинів і реалізує повний потік даних: від транзакційної системи до аналітичних вітрин.

---

# Огляд Проєкту

Цей проєкт показує, як можна побудувати сучасну data-platform через пошарову архітектуру:

`OLTP -> Staging -> Data Warehouse -> Data Marts`

Пайплайн обробляє дані продажів і готує їх для аналітичних запитів та звітності.

Основні акценти реалізації:

- пошарова архітектура даних
- інкрементальні ETL-пайплайни
- dimensional modeling (fact + dimension tables)
- оркестрація через Airflow
- відтворюване середовище через Docker

---

# Архітектура

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

## Відповідальність Шарів

### OLTP
Операційна транзакційна база, де зберігаються сирі бізнес-події.

### Staging
Проміжний landing-layer для ізоляції джерела та підготовки даних до трансформацій.

### Data Warehouse
Аналітичне сховище у вимірній моделі, оптимізоване під запити.

### Data Marts
Агреговані бізнес-вітрини для звітності й аналітики.

---

# Технологічний Стек

## Мови
- Python
- SQL

## Бази Даних
- PostgreSQL (OLTP + staging)
- ClickHouse (DWH + marts)

## Оркестрація
- Airflow

## Інфраструктура
- Docker

---

# Модель Даних

DWH використовує dimensional modeling.

## Fact-таблиця

```text
fact_sales
```

Містить транзакції продажів із посиланнями на виміри.

## Dimension-таблиці

```text
dim_users
dim_products
```

Містять описові атрибути для аналітичних зрізів.

---

# Потік Pipeline

Пайплайн складається з трьох логічних етапів.

## 1. OLTP -> Staging

Інкрементальна синхронізація з операційної бази.

Ключові характеристики:
- watermark-based incremental loading
- UPSERT-логіка
- ізоляція джерела

---

## 2. Staging -> Data Warehouse

Трансформація і завантаження у вимірну схему.

Основні кроки:
- завантаження вимірів
- наповнення fact-таблиці
- перевірки якості даних

---

## 3. Data Warehouse -> Data Marts

Агрегаційний шар для аналітичних запитів.

Реалізовані вітрини:

```text
sales_daily
sales_by_product
sales_by_city
sales_by_user
```

---

# Структура Проєкту

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

# Як Запустити

## 1. Налаштувати Оточення

PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

## 2. Запустити Сервіси

```bash
docker compose up -d
```

## 3. Підключитися до PostgreSQL

- Host: `127.0.0.1`
- Port: `54321`
- Database: `sql_practice`
- User: `postgres`
- Password: `postgres`

Кастомний зовнішній порт `54321` використовується, щоб уникнути конфлікту з локальним PostgreSQL на `5432`.

## 4. Підключитися до ClickHouse

- Host: `127.0.0.1`
- HTTP Port: `81234`
- User: `admin`
- Password: `adminpass`
- Database: `dwh`

## 5. Відкрити Airflow

- URL: `http://localhost:8090`
- Login: `admin`
- Password: `admin`

Увімкни DAG `dwh_pipeline` і запусти його вручну.

---

# Очікуваний Результат

Після успішного виконання пайплайна всі Airflow-задачі:

```text
raw_etl
dwh_etl
refresh_marts
```

мають завершитися зі статусом success.

Дані з'являються у шарах:

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

# Ключові Інженерні Рішення

## PostgreSQL для OLTP
Обрано як просту транзакційну базу для моделювання роботи retail-системи.

## ClickHouse для Аналітики
Оптимізований для аналітичних навантажень і великих агрегацій.

## Staging-шар
Розв'язує залежність між схемою джерела і аналітичними трансформаціями.

## Інкрементальне Завантаження
Підхід на watermark зменшує обсяг перезавантажень і час обробки.

## Оркестрація через Airflow
Дає видимість виконання пайплайна та залежностей між задачами.

---

# Чому Я Навчився

У межах проєкту я опрацював:

- пошарову архітектуру data-platform
- dimensional modeling для аналітики
- дизайн інкрементального ETL
- оркестрацію пайплайнів через Airflow
- побудову відтворюваного локального середовища через Docker

---

# Проблеми, Які Було Вирішено

- конфлікт timezone у інкрементальних завантаженнях
- конфлікти контейнерних і локальних портів
- узгодження схем між SQL-ініціалізацією і ETL-кодом

---

# Приклади Даних

Приклади зрізів для кожного шару знаходяться у:

```text
data_examples/
```

Ці приклади показують, як дані проходять шлях від OLTP-записів до аналітичних вітрин.
