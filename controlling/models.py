from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

EMPLOYMENT_STATUS = (
    ('open', 'Otwarta'),
    ('paused', 'Wstrzymana'),
    ('closed', 'Zakończona')
)

JOB_LEVELS = (
    ('junior', 'Asystent / Technik / Stażysta'),  # fully dependent employee
    ('mid', 'Inżynier / Kordynator'),
    ('senior', 'Projektant / Project Manager'),  # independent employee
    ('expert', 'Kierownik / Ekspert')
)


class Employee(models.Model):
    """Dane, parametry, i masa innych rzeczy związana z Pracownikiem"""
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True,
                                blank=True)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=30)
    workStatus = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS,
                                  default='open')
    jobtitle = models.CharField(max_length=30)
    joblevel = models.CharField(max_length=30, choices=JOB_LEVELS,
                                default='junior')
    workStart = models.DateField(default=timezone.now())
    workEnd = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.firstName} {self.lastName}"
