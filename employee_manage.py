
import unittest
from unittest.mock import patch

#  module "employee_manage.py"
class Employee:
    def __init__(self):
        self.name = "admin"

    def check_employee(self, name):
        self.call_database(name)
        return True

    def add_task(self, tasks):
        for task in tasks:
            msg = self.get_report(task)
            print(msg)
        return True

    def call_database(self, name): # pragma: no cover
        print("Calling database")

    def get_report(self, task): # pragma: no cover
        print("Getting report...")
