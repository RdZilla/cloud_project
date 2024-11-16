from django.urls import path

from organization.views import EmployeesView, EmployeeView

urlpatterns = [
    path("employee", EmployeesView.as_view(), name="employees"),
    path("employee/<str:pk>", EmployeeView.as_view(), name="employee by id"),

]
