"""
### DAG Documentation
이 DAG는 BigqueryPartitionSensor를 사용하는 예제입니다.
"""
from __future__ import annotations

from textwrap import dedent

import pendulum
from airflow import DAG
from airflow.providers.sktvane.sensors.gcp import BigqueryPartitionSensor


with DAG(
    "dag_bigquery_partition_sensor",
    default_args={"retries": 2},
    description="DAG with own plugins",
    schedule="*/30 * * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["demo"],
) as dag:

    dag.doc_md = __doc__

    sensor = BigqueryPartitionSensor(
        task_id=f"check_bq_partition",
        dataset_id="loc",
        table_id="ob_roaming_country",
        partition="dt = '2023-04-01'",
        mode="reschedule",
        poke_interval=60 * 10,
        timeout=60 * 60 * 3,
        dag=dag,
        retries=3,
    )
    sensor.doc_md = dedent(
        """\
    #### BigQuery Partition Sensor Task
    BigQueryPartitionSensor 사용 예제
    """
    )
