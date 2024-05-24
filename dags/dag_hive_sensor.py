"""
### DAG Documentation
이 DAG는 HivePartitionSensor를 사용하는 예제입니다.
"""
from __future__ import annotations

from textwrap import dedent

import pendulum
from airflow import DAG
from airflow.sensors.hive_partition_sensor import HivePartitionSensor


with DAG(
    "dag_hive_partition_sensor",
    default_args={"retries": 2},
    description="DAG with own plugins",
    schedule="*/30 * * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["demo"],
) as dag:

    dag.doc_md = __doc__

    sensor = HivePartitionSensor(
        task_id="check_hive_partition",
        table="ob_roaming_country",
        partition=f"dt='20230401'",
        schema="saturn",
        mode="reschedule",
        poke_interval=60 * 10,
        timeout=60 * 60 * 24,
        dag=dag
    )
    sensor.doc_md = dedent(
        """\
    #### Hive Partition Sensor Task
    HivePartitionSensor 사용 예제
    """
    )
