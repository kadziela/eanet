from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date

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

MPK_STATUS = (
    ('to_accept', 'Do akceptacji'),
    ('open', 'Otwarty'),
    ('to_colse', 'Do zamknięcia'),
    ('closed', 'Zamknięty')
)

ACTIVITY = (
    ('home', 'Praca z Domu'),
    ('vacation', 'Urlop'),
    ('absence', 'Nieobecność'),
    ('overtimePickup', 'Odbiór nadgodzin'),
    ('partialAbsence', 'Częściowa niedyspozycja'),
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
    workStart = models.DateField(default=timezone.now)
    workEnd = models.DateField(blank=True, null=True)

    def save(self):
        super(Employee, self).save()
        employeeWorkSheet = EmployeeWorkSheet(
            employee=self, month=date(self.workStart.year,
                                      self.workStart.month, 1))
        employeeWorkSheet.save()

    def __str__(self) -> str:
        return f"{self.firstName} {self.lastName}"


class MPK(models.Model):
    """Miejsce powstania Kosztu"""
    number = models.CharField(max_length=6)
    description = models.CharField(max_length=100)
    createdDate = models.DateTimeField(auto_now_add=True)
    updatedDate = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=MPK_STATUS,
                              default='to_accept')
    declaredEndDate = models.DateField()

    def __str__(self) -> str:
        return f"{self.number}"


class EmployeeWorkSheet(models.Model):
    """Arkusz godzin"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()
    editable = models.BooleanField(default=True)

    class Meta:
        unique_together = ('employee', 'month')

    def __str__(self) -> str:
        return f"{self.employee}_{self.month.year}_{self.month.month}"


class MPKWorkSheet(models.Model):
    """Godzinki na MPK, pracownika i miesiąc"""
    employeeWorkHourSheet = models.ForeignKey(EmployeeWorkSheet,
                                              on_delete=models.CASCADE)
    mpk = models.ForeignKey(MPK, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('employeeWorkHourSheet', 'mpk')

    def __str__(self) -> str:
        return f"{self.employeeWorkHourSheet}_{self.mpk}"


class HourOfWorkSheet(models.Model):
    """Number of hours worked in the day"""
    mpkWorkSheet = models.ForeignKey(MPKWorkSheet,
                                     on_delete=models.CASCADE)
    day = models.DateField()
    numberOfHours = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('mpkWorkSheet', 'day')

    def __str__(self) -> str:
        return (
            f"{self.mpkWorkSheet.employeeWorkHourSheet}_{self.day.day}_"
            f"{self.mpkWorkSheet.mpk}"
        )
