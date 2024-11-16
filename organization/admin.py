from django.contrib import admin

from organization.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'last_name', 'first_name', 'position', 'gender']
    search_fields = ['last_name', 'middle_name', 'first_name', 'position']

