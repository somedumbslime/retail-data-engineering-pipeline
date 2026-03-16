from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "data_engineer",
    "start_date": datetime(2026, 1, 1),
    "retries": 0,
}


with DAG(
    dag_id="dwh_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["etl", "dwh"],
) as dag:

    raw_etl = BashOperator(
        task_id="raw_etl",
        bash_command="""
            set -euo pipefail
            cd /opt/airflow/etl
            python -m pipelines.oltp_to_staging
        """,
    )

    dwh_etl = BashOperator(
        task_id="dwh_etl",
        bash_command="""
            set -euo pipefail
            cd /opt/airflow/etl
            python -m pipelines.staging_to_dwh
        """,
    )

    refresh_marts = BashOperator(
        task_id="refresh_marts",
        bash_command="""
            set -euo pipefail
            cd /opt/airflow/etl
            python -m pipelines.marts_refresh
        """,
    )

    raw_etl >> dwh_etl >> refresh_marts
