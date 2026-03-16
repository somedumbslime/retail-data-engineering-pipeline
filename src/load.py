import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

DEFAULT_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/sql_practice"


def get_engine(database_url: str | None = None) -> Engine:
    """Create SQLAlchemy engine for PostgreSQL target."""
    url = database_url or os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
    return create_engine(url)


def _run_sql_script(engine: Engine, script_path: Path) -> None:
    sql_text = script_path.read_text(encoding="utf-8")
    statements = [statement.strip() for statement in sql_text.split(";") if statement.strip()]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


def init_dwh_schema(engine: Engine, dwh_schema_path: Path) -> None:
    _run_sql_script(engine, dwh_schema_path)


def create_marts(engine: Engine, marts_path: Path) -> None:
    _run_sql_script(engine, marts_path)


def load_dim_users(dim_users_df: pd.DataFrame, engine: Engine) -> None:
    with engine.begin() as connection:
        for row in dim_users_df.itertuples(index=False):
            connection.execute(
                text(
                    """
                    INSERT INTO dim_users (source_user_id, user_name, city, created_at)
                    VALUES (:source_user_id, :user_name, :city, :created_at)
                    ON CONFLICT (source_user_id)
                    DO UPDATE SET
                        user_name = EXCLUDED.user_name,
                        city = EXCLUDED.city;
                    """
                ),
                {
                    "source_user_id": int(row.user_id),
                    "user_name": row.user_name,
                    "city": row.city,
                    "created_at": row.created_at.to_pydatetime(),
                },
            )


def load_dim_products(dim_products_df: pd.DataFrame, engine: Engine) -> None:
    with engine.begin() as connection:
        for row in dim_products_df.itertuples(index=False):
            connection.execute(
                text(
                    """
                    INSERT INTO dim_products (source_product_id, product_name, category, created_at)
                    VALUES (:source_product_id, :product_name, :category, :created_at)
                    ON CONFLICT (source_product_id)
                    DO UPDATE SET
                        product_name = EXCLUDED.product_name,
                        category = EXCLUDED.category;
                    """
                ),
                {
                    "source_product_id": int(row.product_id),
                    "product_name": row.product_name,
                    "category": row.category,
                    "created_at": row.created_at.to_pydatetime(),
                },
            )


def load_fact_sales(fact_sales_df: pd.DataFrame, engine: Engine) -> None:
    with engine.begin() as connection:
        for row in fact_sales_df.itertuples(index=False):
            connection.execute(
                text(
                    """
                    INSERT INTO fact_sales (
                        source_order_id,
                        user_key,
                        product_key,
                        order_date,
                        price,
                        quantity,
                        total_amount
                    )
                    SELECT
                        :source_order_id,
                        du.user_key,
                        dp.product_key,
                        :order_date,
                        :price,
                        :quantity,
                        :total_amount
                    FROM dim_users du
                    JOIN dim_products dp
                      ON du.source_user_id = :source_user_id
                     AND dp.source_product_id = :source_product_id
                    ON CONFLICT (source_order_id)
                    DO UPDATE SET
                        user_key = EXCLUDED.user_key,
                        product_key = EXCLUDED.product_key,
                        order_date = EXCLUDED.order_date,
                        price = EXCLUDED.price,
                        quantity = EXCLUDED.quantity,
                        total_amount = EXCLUDED.total_amount;
                    """
                ),
                {
                    "source_order_id": int(row.source_order_id),
                    "source_user_id": int(row.source_user_id),
                    "source_product_id": int(row.source_product_id),
                    "order_date": row.order_date,
                    "price": float(row.price),
                    "quantity": int(row.quantity),
                    "total_amount": float(row.total_amount),
                },
            )
