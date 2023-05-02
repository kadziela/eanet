from django.test import TestCase
from django.contrib.auth.models import User
from controlling.forms import EmployeeForm, MPKForm
from datetime import date


class TestForm(TestCase):

    def test_employee_form_valid_data(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'

        )
        form = EmployeeForm(data={
            'user': self.user,
            'firstName': 'name1',
            'lastName': 'nastname1',
            'workStatus': 'open',

        })

        self.assertTrue(form.is_valid())

    def test_employee_form_no_data(self):
        form = EmployeeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_mpk_form_valid_data(self):
        form = MPKForm(data={
            'number': 'MPK000',
            'description': 'some description',
            'status': 'to_accept',
            'declaredEndDate': date(2022, 5, 5),

        })

        self.assertTrue(form.is_valid())

    def test_mpk_form_no_data(self):
        form = MPKForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
