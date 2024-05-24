from __future__ import annotations

import pendulum

from airflow import DAG

from airflow.operators.python import PythonOperator

with DAG(
        "dag_mail_alert",
        default_args={"retries": 1},
        description="DAG tutorial",
        schedule="*/30 * * * *",
        start_date=pendulum.datetime(2023, 4, 10, tz="Asia/Seoul"),
        catchup=False,
        tags=["example"],
) as dag:
    def fool_fn(**kwargs):
        assert 1 == 2


    fool_task = PythonOperator(
        task_id="fool_task",
        python_callable=fool_fn,
        email=["test@sktai.io"],
        email_on_retry=True,
        email_on_failure=True,
    )
