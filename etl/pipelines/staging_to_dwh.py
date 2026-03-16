from core.clickhouse_client import get_clickhouse_client
from core.logger import setup_logger
from dwh.data_quality import run_dq_checks
from dwh.loaders import load_dim_products, load_dim_users, load_fact_sales

logger = setup_logger(__name__)


def main():
    logger.info("Starting DWH ETL...")

    try:
        client = get_clickhouse_client()

        load_dim_users(client)
        load_dim_products(client)
        load_fact_sales(client)

        run_dq_checks(client)

        logger.info("DWH ETL finished successfully.")

    except Exception as e:
        logger.exception(f"DWH ETL failed: {e}")
        raise


if __name__ == "__main__":
    main()
