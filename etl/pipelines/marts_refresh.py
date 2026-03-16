from core.clickhouse_client import execute_command, get_clickhouse_client, truncate_table
from core.logger import setup_logger
from marts_layer.transforms import (
    REFRESH_SALES_BY_CITY_SQL,
    REFRESH_SALES_BY_PRODUCT_SQL,
    REFRESH_SALES_BY_USER_SQL,
    REFRESH_SALES_DAILY_SQL,
)

logger = setup_logger(__name__)


def refresh_sales_daily(client):
    logger.info("Refreshing mart.sales_daily...")
    truncate_table(client, "mart.sales_daily")
    execute_command(client, REFRESH_SALES_DAILY_SQL)
    logger.info("mart.sales_daily refreshed.")


def refresh_sales_by_product(client):
    logger.info("Refreshing mart.sales_by_product...")
    truncate_table(client, "mart.sales_by_product")
    execute_command(client, REFRESH_SALES_BY_PRODUCT_SQL)
    logger.info("mart.sales_by_product refreshed.")


def refresh_sales_by_city(client):
    logger.info("Refreshing mart.sales_by_city...")
    truncate_table(client, "mart.sales_by_city")
    execute_command(client, REFRESH_SALES_BY_CITY_SQL)
    logger.info("mart.sales_by_city refreshed.")


def refresh_sales_by_user(client):
    logger.info("Refreshing mart.sales_by_user...")
    truncate_table(client, "mart.sales_by_user")
    execute_command(client, REFRESH_SALES_BY_USER_SQL)
    logger.info("mart.sales_by_user refreshed.")


def main():
    logger.info("Starting marts refresh...")

    try:
        client = get_clickhouse_client()

        refresh_sales_daily(client)
        refresh_sales_by_product(client)
        refresh_sales_by_city(client)
        refresh_sales_by_user(client)

        logger.info("All marts refreshed successfully.")

    except Exception as e:
        logger.exception(f"Marts refresh failed: {e}")
        raise


if __name__ == "__main__":
    main()
