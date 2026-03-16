-- Data marts schema (ClickHouse)
CREATE DATABASE IF NOT EXISTS mart;

CREATE TABLE IF NOT EXISTS mart.sales_daily
(
    order_date Date,
    total_orders UInt32,
    total_items UInt32,
    total_revenue Decimal(12,2)
)
ENGINE = MergeTree
ORDER BY order_date;

CREATE TABLE IF NOT EXISTS mart.sales_by_product
(
    product_id UInt32,
    product_name String,
    product_category String,
    total_quantity UInt32,
    total_revenue Decimal(12,2)
)
ENGINE = MergeTree
ORDER BY (product_category, product_id);

CREATE TABLE IF NOT EXISTS mart.sales_by_city
(
    user_city String,
    total_orders UInt32,
    total_revenue Decimal(12,2)
)
ENGINE = MergeTree
ORDER BY user_city;

CREATE TABLE IF NOT EXISTS mart.sales_by_user
(
    user_name String,
    city String,
    sales_count UInt32,
    total_spent Decimal(12,2)
)
ENGINE = MergeTree
ORDER BY (city, user_name);
