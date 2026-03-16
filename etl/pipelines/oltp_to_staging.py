import psycopg
from psycopg import sql

from core.config import POSTGRES_CONFIG

DB = POSTGRES_CONFIG
TABLES = ["users", "products", "orders", "order_items"]


def get_cols(cur, table: str) -> list[str]:
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'staging' AND table_name = %s
        ORDER BY ordinal_position;
        """,
        (table,),
    )
    return [r[0] for r in cur.fetchall()]


def get_watermark(cur, table: str):
    cur.execute(
        """
        SELECT last_ts, last_id
        FROM etl.watermark
        WHERE table_name = %s;
        """,
        (table,),
    )
    return cur.fetchone()


def set_watermark(cur, table: str, new_ts, new_id: int):
    cur.execute(
        """
        UPDATE etl.watermark
        SET last_ts = %s, last_id = %s, updated_at = now()
        WHERE table_name = %s;
        """,
        (
            new_ts,
            new_id,
            table,
        ),
    )


def upsert_increment(cur, table: str):
    cols = get_cols(cur, table)
    if "updated_at" not in cols:
        raise RuntimeError(
            f"staging.{table} does not contain updated_at. Increment is not available."
        )
    if "id" not in cols:
        raise RuntimeError(
            f"staging.{table} does not contain id - UPSERT is not available."
        )

    last_ts, last_id = get_watermark(cur, table)

    cur.execute(
        sql.SQL(
            """
            SELECT updated_at, id
            FROM public.{t}
            WHERE (updated_at, id) > (%s, %s)
            ORDER BY updated_at DESC, id DESC
            LIMIT 1;
            """
        ).format(t=sql.Identifier(table)),
        (last_ts, last_id),
    )
    boundary = cur.fetchone()
    if boundary is None:
        return 0

    max_ts, max_id = boundary

    cols_sql = sql.SQL(",").join(map(sql.Identifier, cols))
    set_clause = sql.SQL(",").join(
        sql.SQL("{c}=EXCLUDED.{c}").format(c=sql.Identifier(c))
        for c in cols
        if c != "id"
    )

    q = sql.SQL(
        """
        INSERT INTO staging.{t} ({cols})
        SELECT {cols}
        FROM public.{t}
        WHERE (updated_at, id) > (%s, %s)
            AND (updated_at, id) <= (%s, %s)
        ON CONFLICT (id) DO UPDATE
        SET {set_clause};
        """
    ).format(
        t=sql.Identifier(table),
        cols=cols_sql,
        set_clause=set_clause,
    )

    cur.execute(q, (last_ts, last_id, max_ts, max_id))
    affected = cur.rowcount

    set_watermark(cur, table, max_ts, max_id)

    return affected


def main():
    with psycopg.connect(**DB) as conn:
        with conn.cursor() as cur:
            total = 0
            for table_name in TABLES:
                total += upsert_increment(cur, table_name)

    print(f"OK. processed_rows={total}")


if __name__ == "__main__":
    main()
