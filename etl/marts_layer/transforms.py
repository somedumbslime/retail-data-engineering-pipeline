REFRESH_SALES_DAILY_SQL = """
INSERT INTO mart.sales_daily
SELECT
    order_date,
    toUInt32(uniqExact(order_id)) AS total_orders,
    toUInt32(sum(quantity)) AS total_items,
    toDecimal32(sum(revenue), 2) AS total_revenue
FROM dwh.fact_sales
GROUP BY order_date
ORDER BY order_date;
"""


REFRESH_SALES_BY_PRODUCT_SQL = """
INSERT INTO mart.sales_by_product
SELECT
    product_id,
    product_name,
    product_category,
    toUInt32(sum(quantity)) AS total_quantity,
    toDecimal32(sum(revenue), 2) AS total_revenue
FROM dwh.fact_sales
GROUP BY
    product_id,
    product_name,
    product_category;
"""


REFRESH_SALES_BY_CITY_SQL = """
INSERT INTO mart.sales_by_city
SELECT
    user_city,
    toUInt32(uniqExact(order_id)) AS total_orders,
    toDecimal32(sum(revenue), 2) AS total_revenue
FROM dwh.fact_sales
GROUP BY user_city;
"""


REFRESH_SALES_BY_USER_SQL = """
INSERT INTO mart.sales_by_user
SELECT
    du.name AS user_name,
    du.city AS city,
    toUInt32(count()) AS sales_count,
    toDecimal32(sum(fs.revenue), 2) AS total_spent
FROM dwh.fact_sales fs
JOIN dwh.dim_users du ON fs.user_id = du.user_id
GROUP BY du.name, du.city;
"""
