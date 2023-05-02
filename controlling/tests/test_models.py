from django.test import TestCase
from datetime import date
from controlling.models import (
    Employee, MPK, EmployeeWorkSheet, MPKWorkSheet, HourOfWorkSheet
)


class TestModels(TestCase):

    def setUp(self):
        self.employee1 = Employee.objects.create(
            firstName='name1',
            lastName='lastname1',
            workStatus='open',
            workStart=date(2023, 5, 2)

        )

    def test_autocreate_emploteeworksheet(self):
        self.employeeworksheet1 = EmployeeWorkSheet.objects.filter(
            employee=self.employee1)[0]
        self.assertEqual(self.employeeworksheet1.employee, self.employee1)
        self.assertEqual(self.employeeworksheet1.month, date(2023, 5, 1))
        self.assertEqual(self.employeeworksheet1.editable, True)
