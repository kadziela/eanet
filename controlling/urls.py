from django.urls import path
from .views import (
    home, login_request, logout_request, administration_panel, mpk_add,
    employee_add, employee_list, mpk_list, worksheets_list, worksheet_edit
)

urlpatterns = [
    path('', home, name="home"),
    path('administration-panel', administration_panel,
         name="administration_panel"),
    path('login', login_request, name="login"),
    path('logout', logout_request, name="logout"),
    path('employee-add', employee_add, name="employee_add"),
    path('mpk-add', mpk_add, name="mpk_add"),
    path('employee-list', employee_list, name="employee_list"),
    path('mpk-list', mpk_list, name="mpk_list"),
    path('worksheets-list', worksheets_list, name="worksheets_list"),
    path('worksheet-edit/<str:pk>', worksheet_edit, name="worksheet_edit"),

]
