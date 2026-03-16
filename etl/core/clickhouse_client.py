import clickhouse_connect

from core.config import CLICKHOUSE_CONFIG
from core.logger import setup_logger

logger = setup_logger(__name__)


def get_clickhouse_client():
    try:
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_CONFIG["host"],
            port=CLICKHOUSE_CONFIG["port"],
            username=CLICKHOUSE_CONFIG["username"],
            password=CLICKHOUSE_CONFIG["password"],
            database=CLICKHOUSE_CONFIG["database"],
        )
        logger.info("ClickHouse client established.")
        return client
    except Exception as e:
        logger.exception(f"Failed to create ClickHouse client: {e}")
        raise


def truncate_table(client, table_name: str):
    try:
        logger.info(f"Truncating ClickHouse table: {table_name}")
        client.command(f"TRUNCATE TABLE {table_name}")
    except Exception as e:
        logger.exception(f"Failed to truncate table {table_name}: {e}")
        raise


def insert_data(client, table_name: str, rows: list, column_names: list[str]):
    try:
        if not rows:
            logger.warning(f"No data to insert into {table_name}")
            return

        logger.info(f"Inserting {len(rows)} rows into {table_name}")
        client.insert(table_name, rows, column_names=column_names)

    except Exception as e:
        logger.exception(f"Failed to insert data into {table_name}: {e}")
        raise


def execute_command(client, query: str):
    try:
        logger.info("Executing ClickHouse command")
        client.command(query)
    except Exception as e:
        logger.exception(f"Failed to execute ClickHouse command: {e}")
        raise
