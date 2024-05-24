from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class MyOwnOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 connection="connection if needed",
                 param="parameter if needed",
                 *args, **kwargs):

        super(MyOwnOperator, self).__init__(*args, **kwargs)
        # Store attributes in class
        self.connection = connection
        self.param = param

    def execute(self, context):
        self.log.info("Airflow!")
        self.log.error("SaaS!!")
        self.log.warning("Vane!!!")
