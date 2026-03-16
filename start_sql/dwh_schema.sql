-- DWH / OLAP schema (ClickHouse)
CREATE DATABASE IF NOT EXISTS dwh;

CREATE TABLE IF NOT EXISTS dwh.dim_users
(
    user_id UInt32,
    name String,
    email String,
    city String,
    created_at DateTime
)
ENGINE = MergeTree
ORDER BY user_id;

CREATE TABLE IF NOT EXISTS dwh.dim_products
(
    product_id UInt32,
    name String,
    category String,
    price Decimal(10,2)
)
ENGINE = MergeTree
ORDER BY product_id;

CREATE TABLE IF NOT EXISTS dwh.fact_sales
(
    order_id UInt32,
    user_id UInt32,
    product_id UInt32,
    user_city String,
    product_name String,
    product_category String,
    order_date Date,
    quantity UInt32,
    price_at_purchase Decimal(10,2),
    revenue Decimal(12,2)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(order_date)
ORDER BY (order_date, product_id, user_id, order_id);
