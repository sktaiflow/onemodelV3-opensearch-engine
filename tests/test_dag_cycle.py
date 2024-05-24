import configparser as parser
import logging
import os

import pytest
from airflow.models import DagBag

logger = logging.getLogger(__name__)


class TestDagsCycle:
    @pytest.fixture
    def meta_db_mock(self, mocker):
        return mocker.patch("airflow.models.Variable.get", return_value="dev")

    @pytest.fixture
    def home_path(self):
        home_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return home_path

    @pytest.fixture
    def exception_dag(self, home_path):
        properties = parser.ConfigParser(allow_no_value=True)
        properties.read(f"{home_path}/tests/.dagtestignore")
        full_paths = list(
            map(
                lambda x: f"{home_path}/dags/{x[0]}",
                properties.items("test_excluded_dag"),
            )
        )
        return full_paths

    @pytest.fixture
    def dag_list(self, home_path, exception_dag):
        dag_list = []
        for path, directories, files in os.walk(f"{home_path}/dags"):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                full_path = os.path.join(path, filename)
                if ext == ".py" and full_path not in exception_dag:
                    dag_list.append(full_path)
        return dag_list

    def test_dag_import_error(self, meta_db_mock, home_path, dag_list):
        import_error_list = []
        for dag_path in dag_list:
            dag_bag = DagBag(dag_folder=dag_path, include_examples=False)
            if dag_bag.import_errors:
                import_error_list.append(dag_bag.import_errors)

        try:
            assert len(import_error_list) == 0
        except AssertionError as e:
            for error_case in import_error_list:
                for k, v in error_case.items():
                    logger.error(f"Import Error Key: {k}")
                    logger.error(f"Import Error Value: {v}")
            raise e
