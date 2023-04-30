from django.contrib import admin
from .models import (
    Employee, MPK, EmployeeWorkSheet, MPKWorkSheet, HourOfWorkSheet
)

# Register your models here.


class HourOfWorkSheetInLine(admin.StackedInline):
    model = HourOfWorkSheet


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["__str__", "user", "workStatus"]
    list_filter = ["workStatus"]
    search_fields = ["firstName", "lastName"]


@admin.register(EmployeeWorkSheet)
class EmployeeWorkSheetAdmin(admin.ModelAdmin):
    search_fields = ["employee", "month"]


@admin.register(MPKWorkSheet)
class MPKWorkSheetAdmin(admin.ModelAdmin):
    search_fields = ["employeeWorkHourSheet", "mpk"]
    inlines = [
        HourOfWorkSheetInLine
    ]


admin.site.register(MPK)
