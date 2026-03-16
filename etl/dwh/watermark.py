import psycopg

from core.config import POSTGRES_CONFIG


def get_postgres_connection():
    return psycopg.connect(**POSTGRES_CONFIG)


def get_dwh_watermark(table_name: str):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT last_ts, last_id
                FROM etl.dwh_watermark
                WHERE table_name = %s;
                """,
                (table_name,),
            )
            return cur.fetchone()


def set_dwh_watermark(table_name: str, new_ts, new_id: int):
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE etl.dwh_watermark
                SET last_ts = %s,
                    last_id = %s,
                    updated_at = now()
                WHERE table_name = %s;
                """,
                (new_ts, new_id, table_name),
            )
        conn.commit()


def get_fact_sales_boundary():
    with get_postgres_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT updated_at AT TIME ZONE 'UTC', id
                FROM staging.order_items
                ORDER BY updated_at DESC, id DESC
                LIMIT 1;
                """
            )
            return cur.fetchone()
