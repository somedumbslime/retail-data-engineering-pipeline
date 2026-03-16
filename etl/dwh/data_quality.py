from core.logger import setup_logger

logger = setup_logger(__name__)


def check_no_nulls(client, table_name: str, columns: list[str]):
    for column in columns:
        query = f"""
        SELECT count()
        FROM {table_name}
        WHERE {column} IS NULL
        """
        result = client.query(query)
        null_count = result.first_item["count()"]

        if null_count > 0:
            raise ValueError(
                f"Data quality check failed: {table_name}.{column} contains {null_count} NULLs"
            )

        logger.info(f"DQ passed: {table_name}.{column} has no NULLs")


def check_no_duplicates(client, table_name: str, key_columns: list[str]):
    keys = ", ".join(key_columns)

    query = f"""
    SELECT count()
    FROM (
        SELECT {keys}, count() as cnt
        FROM {table_name}
        GROUP BY {keys}
        HAVING cnt > 1
    )
    """
    result = client.query(query)
    duplicate_count = result.first_item["count()"]

    if duplicate_count > 0:
        raise ValueError(
            f"Data quality check failed: {table_name} contains {duplicate_count} duplicate keys by ({keys})"
        )

    logger.info(f"DQ passed: {table_name} has no duplicates by ({keys})")


def check_fact_sales_revenue(client):
    query = """
    SELECT count()
    FROM dwh.fact_sales
    WHERE revenue != quantity * price_at_purchase
    """
    result = client.query(query)
    bad_rows = result.first_item["count()"]

    if bad_rows > 0:
        raise ValueError(
            f"Data quality check failed: fact_sales contains {bad_rows} rows with invalid revenue"
        )

    logger.info("DQ passed: fact_sales.revenue is valid")


def check_fact_sales_positive_values(client):
    query = """
    SELECT count()
    FROM dwh.fact_sales
    WHERE quantity <= 0 OR price_at_purchase < 0
    """
    result = client.query(query)
    bad_rows = result.first_item["count()"]

    if bad_rows > 0:
        raise ValueError(
            f"Data quality check failed: fact_sales contains {bad_rows} invalid numeric rows"
        )

    logger.info("DQ passed: fact_sales numeric values are valid")



def run_dq_checks(client):
    logger.info("Starting data quality checks...")

    check_no_nulls(client, "dwh.dim_users", ["user_id"])
    check_no_duplicates(client, "dwh.dim_users", ["user_id"])

    check_no_nulls(client, "dwh.dim_products", ["product_id"])
    check_no_duplicates(client, "dwh.dim_products", ["product_id"])

    check_no_nulls(
        client,
        "dwh.fact_sales",
        ["order_id", "user_id", "product_id", "order_date"]
    )
    check_no_duplicates(client, "dwh.fact_sales", ["order_id", "product_id"])
    check_fact_sales_revenue(client)
    check_fact_sales_positive_values(client)

    logger.info("All data quality checks passed.")
