import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATHS = [PROJECT_ROOT / ".env", PROJECT_ROOT / "etl" / ".env"]

if load_dotenv is not None:
    for env_path in ENV_PATHS:
        if env_path.exists():
            load_dotenv(env_path, override=False)


POSTGRES_CONFIG = {
    "host": os.getenv("APP_POSTGRES_HOST", "localhost"),
    "dbname": os.getenv("APP_POSTGRES_DB", "sql_practice"),
    "user": os.getenv("APP_POSTGRES_USER", "postgres"),
    "password": os.getenv("APP_POSTGRES_PASSWORD", "postgres"),
    "port": int(os.getenv("APP_POSTGRES_PORT", 5432)),
}

CLICKHOUSE_CONFIG = {
    "host": os.getenv("APP_CLICKHOUSE_HOST", "localhost"),
    "port": int(os.getenv("APP_CLICKHOUSE_PORT", 8123)),
    "username": os.getenv("APP_CLICKHOUSE_USER", "admin"),
    "password": os.getenv("APP_CLICKHOUSE_PASSWORD", "adminpass"),
    "database": os.getenv("APP_CLICKHOUSE_DB", "dwh"),
}

LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
}
