CREATE SCHEMA IF NOT EXISTS etl;

CREATE TABLE IF NOT EXISTS etl.watermark (
    table_name text PRIMARY KEY,
    last_ts timestamptz NOT NULL,
    last_id bigint NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO etl.watermark (table_name, last_ts, last_id)
VALUES
    ('users', '1970-01-01 00:00:00+00', 0),
    ('products', '1970-01-01 00:00:00+00', 0),
    ('orders', '1970-01-01 00:00:00+00', 0),
    ('order_items', '1970-01-01 00:00:00+00', 0)
ON CONFLICT (table_name) DO NOTHING;

CREATE TABLE IF NOT EXISTS etl.dwh_watermark (
    table_name text PRIMARY KEY,
    last_ts timestamptz NOT NULL,
    last_id bigint NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO etl.dwh_watermark (table_name, last_ts, last_id)
VALUES ('fact_sales', '1970-01-01 00:00:00+00', 0)
ON CONFLICT (table_name) DO NOTHING;
