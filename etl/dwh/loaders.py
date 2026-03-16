from core.clickhouse_client import insert_data, truncate_table
from core.logger import setup_logger
from core.postgres_client import fetch_batches
from dwh.transforms import DIM_PRODUCTS_SQL, DIM_USERS_SQL, FACT_SALES_INCREMENTAL_SQL
from dwh.watermark import get_dwh_watermark, get_fact_sales_boundary, set_dwh_watermark

logger = setup_logger(__name__)


def load_dim_users(client):
    logger.info("Loading dim_users...")
    try:
        truncate_table(client, "dwh.dim_users")

        total = 0

        for batch in fetch_batches(DIM_USERS_SQL):
            insert_data(
                client,
                "dwh.dim_users",
                batch,
                ["user_id", "name", "email", "city", "created_at"]
            )
            total += len(batch)

        logger.info(f"dim_users loaded: {total} rows")

    except Exception as e:
        logger.exception(f"Failed to load dim_users: {e}")
        raise


def load_dim_products(client):
    logger.info("Loading dim_products...")
    try:
        truncate_table(client, "dwh.dim_products")

        total = 0

        for batch in fetch_batches(DIM_PRODUCTS_SQL):
            insert_data(
                client,
                "dwh.dim_products",
                batch,
                ["product_id", "name", "category", "price"]
            )
            total += len(batch)

        logger.info(f"dim_products loaded: {total} rows")

    except Exception as e:
        logger.exception(f"Failed to load dim_products: {e}")
        raise


def load_fact_sales(client):
    logger.info("Loading fact_sales incrementally...")
    try:
        last_ts, last_id = get_dwh_watermark("fact_sales")
        boundary = get_fact_sales_boundary()

        if boundary is None:
            logger.info("fact_sales: no data in staging.order_items")
            return

        max_ts, max_id = boundary

        if (max_ts, max_id) <= (last_ts, last_id):
            logger.info("fact_sales: no new rows to load")
            return

        total = 0

        for batch in fetch_batches(
            FACT_SALES_INCREMENTAL_SQL,
            (last_ts, last_id, max_ts, max_id)
        ):
            cleaned_batch = [row[:-2] for row in batch]

            insert_data(
                client,
                "dwh.fact_sales",
                cleaned_batch,
                [
                    "order_id",
                    "user_id",
                    "product_id",
                    "user_city",
                    "product_name",
                    "product_category",
                    "order_date",
                    "quantity",
                    "price_at_purchase",
                    "revenue",
                ]
            )
            total += len(cleaned_batch)

        set_dwh_watermark("fact_sales", max_ts, max_id)
        logger.info(f"fact_sales loaded incrementally: {total} rows")

    except Exception as e:
        logger.exception(f"Failed to load fact_sales incrementally: {e}")
        raise
