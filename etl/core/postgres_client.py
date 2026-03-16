import psycopg

from core.config import POSTGRES_CONFIG
from core.logger import setup_logger

logger = setup_logger(__name__)


def get_postgres_connection():
    try:
        conn = psycopg.connect(**POSTGRES_CONFIG)
        logger.info("Postgres connection established.")
        return conn
    except Exception as e:
        logger.exception(f"Failed to connect to Postgres: {e}")
        raise


def fetch_batches(query: str, params: tuple = (), batch_size: int = 10000):
    try:
        with get_postgres_connection() as conn:
            with conn.cursor() as cur:
                logger.info(
                    f"Executing Postgres batch query with batch_size={batch_size}"
                )
                cur.execute(query, params)

                while True:
                    rows = cur.fetchmany(batch_size)

                    if not rows:
                        break

                    logger.info(f"Fetched batch from Postgres: {len(rows)} rows")
                    yield rows

    except Exception as e:
        logger.exception(f"Failed during batch fetch from Postgres: {e}")
        raise
