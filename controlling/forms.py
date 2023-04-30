from django import forms
from .models import Employee, MPK


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'firstName', 'lastName', 'workStatus']


class MPKForm(forms.ModelForm):
    class Meta:
        model = MPK
        fields = ['number', 'description', 'status', 'declaredEndDate']
