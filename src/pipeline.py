import argparse
from pathlib import Path

from extract import extract_orders, extract_products, extract_users
from load import (
    create_marts,
    get_engine,
    init_dwh_schema,
    load_dim_products,
    load_dim_users,
    load_fact_sales,
)
from transform import clean_data, prepare_dimensions, prepare_fact_table

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = PROJECT_ROOT / "sql"


def run_pipeline(database_url: str | None = None, dry_run: bool = False) -> None:
    orders_df = extract_orders()
    users_df = extract_users(orders_df)
    products_df = extract_products(orders_df)

    clean_orders_df = clean_data(orders_df)
    dim_users_df, dim_products_df = prepare_dimensions(users_df, products_df)
    fact_sales_df = prepare_fact_table(clean_orders_df)

    if dry_run:
        print("Dry run completed successfully")
        print(f"orders={len(clean_orders_df)}")
        print(f"dim_users={len(dim_users_df)}")
        print(f"dim_products={len(dim_products_df)}")
        print(f"fact_sales={len(fact_sales_df)}")
        return

    engine = get_engine(database_url)
    init_dwh_schema(engine, SQL_DIR / "dwh_schema.sql")

    load_dim_users(dim_users_df, engine)
    load_dim_products(dim_products_df, engine)
    load_fact_sales(fact_sales_df, engine)

    create_marts(engine, SQL_DIR / "marts.sql")
    print("Pipeline finished: data loaded into DWH and marts were refreshed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retail ETL pipeline runner")
    parser.add_argument("--database-url", type=str, default=None, help="SQLAlchemy database URL")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run extract/transform only and print row counts.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(database_url=args.database_url, dry_run=args.dry_run)
