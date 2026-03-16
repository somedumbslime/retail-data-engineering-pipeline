from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "sample_data.csv"


def extract_orders(data_path: Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load source sales data and assign technical order ids."""
    orders = pd.read_csv(data_path)
    orders["order_id"] = range(1, len(orders) + 1)
    return orders[["order_id", "user_id", "product_id", "price", "quantity", "date"]]


def extract_users(orders_df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Build a lightweight users dataset from order stream."""
    if orders_df is None:
        orders_df = extract_orders()

    unique_users = sorted(orders_df["user_id"].dropna().astype(int).unique())
    cities = ["Kyiv", "Lviv", "Odesa", "Dnipro", "Kharkiv"]

    return pd.DataFrame(
        {
            "user_id": unique_users,
            "user_name": [f"User {user_id}" for user_id in unique_users],
            "city": [cities[idx % len(cities)] for idx, _ in enumerate(unique_users)],
        }
    )


def extract_products(orders_df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Build a lightweight products dataset from order stream."""
    if orders_df is None:
        orders_df = extract_orders()

    unique_products = sorted(orders_df["product_id"].dropna().astype(int).unique())
    categories = ["Grocery", "Electronics", "Home", "Beauty"]

    return pd.DataFrame(
        {
            "product_id": unique_products,
            "product_name": [f"Product {product_id}" for product_id in unique_products],
            "category": [categories[idx % len(categories)] for idx, _ in enumerate(unique_products)],
        }
    )
