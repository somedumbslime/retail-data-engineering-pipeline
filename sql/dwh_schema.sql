-- DWH schema
CREATE TABLE IF NOT EXISTS dim_users (
    user_key BIGSERIAL PRIMARY KEY,
    source_user_id BIGINT NOT NULL UNIQUE,
    user_name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_products (
    product_key BIGSERIAL PRIMARY KEY,
    source_product_id BIGINT NOT NULL UNIQUE,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fact_sales (
    sale_key BIGSERIAL PRIMARY KEY,
    source_order_id BIGINT NOT NULL UNIQUE,
    user_key BIGINT NOT NULL REFERENCES dim_users(user_key),
    product_key BIGINT NOT NULL REFERENCES dim_products(product_key),
    order_date DATE NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    total_amount NUMERIC(12, 2) NOT NULL,
    loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
