import pandas as pd


def clean_data(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Apply basic quality checks and cast source fields."""
    cleaned = orders_df.copy()

    cleaned["price"] = pd.to_numeric(cleaned["price"], errors="coerce")
    cleaned["quantity"] = pd.to_numeric(cleaned["quantity"], errors="coerce")
    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")

    cleaned = cleaned.dropna(subset=["user_id", "product_id", "price", "quantity", "date"])
    cleaned = cleaned[(cleaned["price"] >= 0) & (cleaned["quantity"] > 0)]

    cleaned["user_id"] = cleaned["user_id"].astype(int)
    cleaned["product_id"] = cleaned["product_id"].astype(int)
    cleaned["quantity"] = cleaned["quantity"].astype(int)
    cleaned["date"] = cleaned["date"].dt.date

    return cleaned


def prepare_dimensions(
    users_df: pd.DataFrame, products_df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Prepare conformed dimensions for the DWH layer."""
    dim_users = users_df.drop_duplicates(subset=["user_id"]).copy()
    dim_users["created_at"] = pd.Timestamp.utcnow()

    dim_products = products_df.drop_duplicates(subset=["product_id"]).copy()
    dim_products["created_at"] = pd.Timestamp.utcnow()

    return dim_users, dim_products


def prepare_fact_table(clean_orders_df: pd.DataFrame) -> pd.DataFrame:
    """Create fact-ready sales rows with derived revenue metric."""
    fact_sales = clean_orders_df.copy()
    fact_sales["total_amount"] = (fact_sales["price"] * fact_sales["quantity"]).round(2)

    fact_sales = fact_sales.rename(
        columns={
            "order_id": "source_order_id",
            "user_id": "source_user_id",
            "product_id": "source_product_id",
            "date": "order_date",
        }
    )

    return fact_sales[
        [
            "source_order_id",
            "source_user_id",
            "source_product_id",
            "order_date",
            "price",
            "quantity",
            "total_amount",
        ]
    ]
