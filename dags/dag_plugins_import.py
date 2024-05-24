"""
### Description

- apache-airflow-providers-sktvane 패키지 유효성 검사
"""
from datetime import datetime

from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.operators.python import PythonOperator
from macros.slack import get_slack_notifier


def _test():
    raise AirflowException("AirflowException has occurred!")


with DAG(
    dag_id="dag_plugins_import",
    schedule_interval=None,
    default_args={
        "owner": "홍길동",
        "start_date": datetime(2023, 5, 17),
        "on_failure_callback": get_slack_notifier(slack_email="test@sk.com"),
    },
    catchup=False,
) as dag:
    PythonOperator(task_id="temp", python_callable=_test)

dag.doc_md = __doc__
