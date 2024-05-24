"""
### DAG Documentation
이 DAG는 plugins를 사용하는 예제입니다.
"""
from __future__ import annotations

from textwrap import dedent

import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

from hooks.my_hooks import MyOwnHook
from operators.my_operators import MyOwnOperator

with DAG(
    "dag_with_plugins",
    default_args={"retries": 2},
    description="DAG with own plugins",
    schedule="*/20 * * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["demo"],
) as dag:

    dag.doc_md = __doc__

    def task_my_hook(**kwargs):
        my_hook = MyOwnHook("Vane")
        print(my_hook.act_no_1("first"))
        print(my_hook.act_no_2("second"))


    hook_task = PythonOperator(
        task_id="Test_MyOwnHook",
        python_callable=task_my_hook,
    )
    hook_task.doc_md = dedent(
        """\
    #### Hook task
    Custom Hook을 활용한 task 예제
    """
    )

    operator_task = MyOwnOperator(
        task_id="Test_MyOwnOperator", dag=dag, connection="mysql_default", param="param"
    )
    operator_task.doc_md = dedent(
        """\
    #### Operator task
    Custom Operator를 활용한 task 예제
    """
    )

    operator_task >> hook_task
