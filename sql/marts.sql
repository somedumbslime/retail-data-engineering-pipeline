-- Data marts (views)
CREATE OR REPLACE VIEW sales_by_product AS
SELECT
    dp.product_name,
    dp.category,
    SUM(fs.quantity) AS total_quantity,
    SUM(fs.total_amount) AS total_revenue
FROM fact_sales fs
JOIN dim_products dp ON fs.product_key = dp.product_key
GROUP BY dp.product_name, dp.category;

CREATE OR REPLACE VIEW sales_by_user AS
SELECT
    du.user_name,
    du.city,
    COUNT(fs.sale_key) AS sales_count,
    SUM(fs.total_amount) AS total_spent
FROM fact_sales fs
JOIN dim_users du ON fs.user_key = du.user_key
GROUP BY du.user_name, du.city;
