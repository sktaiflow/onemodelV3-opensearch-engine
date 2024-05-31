"""
### DAG Documentation
이 DAG는 plugins를 사용하는 예제입니다.
"""
from __future__ import annotations
from airflow.models import Variable

import pendulum
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator

with DAG(
    dag_id="opensearch-indexing=test",
    default_args={"retries": 2},
    description="DAG with own plugins",
    schedule="*/20 * * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["test"],
) as dag:

    dag.doc_md = __doc__

    test = PythonOperator(
        task_id="test", 
        python_callable='main.py',
        op_kwargs={
            "http_auth_id": Variable.get('http_auth_id'),
            "http_auth_password": Variable.get('http_auth_password'),
            "input_path": Variable.get('index_hdfs_path_temp'),
            "vpce": Variable.get('opensearch_stg_vpce'),
            "env": Variable.get('temp_env'),
        },
        dag=dag
    )
    
    test