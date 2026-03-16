DIM_USERS_SQL = """
SELECT
    id AS user_id,
    name,
    email,
    city,
    created_at
FROM staging.users
ORDER BY id;
"""


DIM_PRODUCTS_SQL = """
SELECT
    id AS product_id,
    name,
    category,
    price
FROM staging.products
ORDER BY id;
"""


FACT_SALES_INCREMENTAL_SQL = """
SELECT
    o.id AS order_id,
    o.user_id,
    oi.product_id,

    COALESCE(u.city, '') AS user_city,
    p.name AS product_name,
    p.category AS product_category,

    o.order_date::date AS order_date,

    oi.quantity,
    oi.price_at_purchase,
    (oi.quantity * oi.price_at_purchase)::numeric(12,2) AS revenue,

    oi.updated_at AT TIME ZONE 'UTC' AS updated_at_utc,
    oi.id AS order_item_id
FROM staging.orders o
JOIN staging.order_items oi ON o.id = oi.order_id
JOIN staging.users u ON o.user_id = u.id
JOIN staging.products p ON oi.product_id = p.id
WHERE ((oi.updated_at AT TIME ZONE 'UTC'), oi.id) > (%s, %s)
  AND ((oi.updated_at AT TIME ZONE 'UTC'), oi.id) <= (%s, %s)
ORDER BY oi.updated_at, oi.id;
"""
