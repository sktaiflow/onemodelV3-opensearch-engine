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
from airflow.sensors.hive_partition_sensor import HivePartitionSensor
from airflow.sensors.web_hdfs_sensor import WebHdfsSensor
from main import main
from airflow.providers.sktvane.operators.nes import NesOperator
from plugins.packages.schema.schema import AirflowVriable

import os

with DAG(
    dag_id="opensearch-indexing-test",
    default_args={"retries": 2},
    description="DAG with own plugins",
    schedule="7 * * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["test"],
) as dag:

    dag.doc_md = __doc__

    def run_main_script(**kwargs):
        http_auth_id = Variable.get('http_auth_id')
        http_auth_password = Variable.get('http_auth_password')
        input_path = Variable.get('index_hdfs_path_temp')
        vpce = Variable.get('opensearch_stg_vpce')
        env = Variable.get('temp_env')
        return AirflowVriable(
            http_auth_id=http_auth_id,
            http_auth_password=http_auth_password,
            input_path=input_path,
            vpce=vpce,
            env=env,
        )

        # main(
        #     http_auth_id=http_auth_id,
        #     http_auth_password=http_auth_password,
        #     input_path=input_path,
        #     vpce=vpce,
        #     env=env
        # )

    start = DummyOperator(task_id='start', dag=dag)

    indexing_input_sensor = WebHdfsSensor(
            task_id="indexing_input_sensor",
            webhdfs_conn_id='default_webhdfs',
            filepath=os.path.join(Variable.get('index_hdfs_path_temp'), "SUCCESS.txt"),
            poke_interval=60 * 1,
            timeout=60 * 60 * 24,
            dag=dag
        )
    
    run_script_task = PythonOperator(
        task_id='run_main_script',
        python_callable=run_main_script,
        provide_context=True,
        dag=dag
    )   

    test = NesOperator(
        task_id="onemodel_data_pipe_step2",
        parameters={"current_dt": "{{ ds_nodash }}", "variables": run_main_script()},
        input_nb="./notebook/indexing.ipynb",
    )

    start >> run_script_task
    start >> indexing_input_sensor
    start >> test