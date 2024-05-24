from abc import ABC

from airflow.hooks.base import BaseHook


class MyOwnHook(BaseHook, ABC):

    def __init__(self, value):
        super().__init__()
        self.value = value

    def act_no_1(self, param):
        return f"Action No 1: {self.value} {param}"

    def act_no_2(self, param):
        return f"Action No 2: {self.value} {param}"
