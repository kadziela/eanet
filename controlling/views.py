from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from .forms import EmployeeForm, MPKForm
from .models import (
    Employee, MPK, EmployeeWorkSheet, MPKWorkSheet, HourOfWorkSheet
)
from calendar import monthrange
from datetime import date

# Create your views here.


class CellOfShedule:

    def __init__(self, activity, day, isDayOff):
        self.day = day
        self.activity = activity
        self.isDayOff = isDayOff

    def __str__(self) -> str:
        return f"{self.day}"


class CellOfWorkSheet:

    def __init__(self, mpk, day, value):
        self.day = day
        self.mpk = mpk
        self.name = f"{self.day}_{self.mpk}"
        self.value = value

    def __str__(self) -> str:
        return f"{self.mpk}"


def home(request):
    return render(request, 'controlling/home.html')


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponseBadRequest("Invalid username or password.")
        else:
            return HttpResponseBadRequest("Invalid username or password.")
    else:
        form = AuthenticationForm()
        return render(request, 'controlling/login.html', {
            'login_form': form
        })


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return HttpResponseRedirect(reverse('home'))


def administration_panel(request):
    return render(request, 'controlling/administration-panel.html')


def employee_add(request):
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administration_panel')
    return render(request, 'controlling/employee-add.html', {
        'form': form
    })


def mpk_add(request):
    form = MPKForm()
    if request.method == 'POST':
        form = MPKForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administration_panel')
    return render(request, 'controlling/mpk-add.html', {
        'form': form
    })


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'controlling/employee-list.html',
                  {'employees': employees})


def mpk_list(request):
    mpks = MPK.objects.all()
    return render(request, 'controlling/mpk-list.html', {'mpks': mpks})


def worksheets_list(request):
    employee = Employee.objects.get(user=request.user)
    worksheets = EmployeeWorkSheet.objects.filter(employee=employee)
    return render(request, 'controlling/worksheets-list.html',
                  {'worksheets': worksheets})


def worksheet_edit(request, pk):
    workHourSheet = EmployeeWorkSheet.objects.get(id=pk)

    if request.method == 'POST' and 'mpkadd' in request.POST:
        mpk = MPK.objects.filter(number=request.POST.get("mpkadd"))[0]
        if mpk is None:
            pass
        else:
            MPKWorkSheet.objects.create(
                employeeWorkHourSheet=workHourSheet, mpk=mpk)

    mpkWorkSheets = MPKWorkSheet.objects.filter(
        employeeWorkHourSheet=workHourSheet)
    mpks = [x.mpk for x in mpkWorkSheets]

    numberOfDays = monthrange(workHourSheet.month.year,
                              workHourSheet.month.month)[1]
    lps = [x+1 for x in range(numberOfDays)]
    dates = [date(workHourSheet.month.year, workHourSheet.month.month, day+1)
             for day in range(numberOfDays)]

    mpksnumber = [x.number for x in mpks]
    allmpks = MPK.objects.exclude(number__in=mpksnumber)

    if request.method == 'POST' and 'mpkadd' not in request.POST:
        for mpk in mpks:
            mpkWorkSheet = MPKWorkSheet.objects.filter(
                mpk=mpk, employeeWorkHourSheet=workHourSheet)[0]
            for day in dates:
                # Jeżeli już istnieje taki objekt
                if len(HourOfWorkSheet.objects.filter(
                        mpkWorkSheet=mpkWorkSheet, day=day)) != 0:
                    if request.POST.get(f"{day}_{mpk}") is (
                            0 or '' or None or '0' or 0.0):
                        HourOfWorkSheet.objects.filter(
                            mpkWorkSheet=mpkWorkSheet, day=day).delete()
                    else:
                        HourOfWorkSheet.objects.filter(
                            mpkWorkSheet=mpkWorkSheet, day=day).update(
                            numberOfHours=float(
                                request.POST.get(f"{day}_{mpk}")))
                else:
                    if request.POST.get(f"{day}_{mpk}") is (
                            0 or '' or None or '0' or 0.0):
                        pass
                    else:
                        HourOfWorkSheet.objects.create(
                            mpkWorkSheet=mpkWorkSheet, day=day,
                            numberOfHours=float(
                                request.POST.get(f"{day}_{mpk}")))

    table = [None]*numberOfDays
    d = 0
    for day in dates:
        table[d] = [lps[d], day, day.strftime("%a")]
        for mpk in mpkWorkSheets:
            if len(HourOfWorkSheet.objects.filter(mpkWorkSheet=mpk,
                                                  day=day)) != 0:
                hour = HourOfWorkSheet.objects.filter(
                    mpkWorkSheet=mpk, day=day)[0]
                cell = CellOfWorkSheet(
                    mpk=mpk.mpk.number, day=day, value=hour.numberOfHours)
            else:
                cell = CellOfWorkSheet(mpk=mpk.mpk.number, day=day, value=0)
            table[d].append(cell)
        d += 1

    context = {
        'mpks': mpks,
        'table': table,
        'dates': dates,
        'allmpks': allmpks,
    }

    return render(request, 'controlling/worksheet-edit.html', context)
