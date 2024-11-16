from django.contrib import admin

from health_alert.models.health_reference_models import EmployeeHealthReference
from health_alert.models.health_measurement_models import EmployeeHealthMeasurement


@admin.register(EmployeeHealthMeasurement)
class EmployeeHealthMeasurementAdmin(admin.ModelAdmin):
    pass

@admin.register(EmployeeHealthReference)
class EmployeeHealthReferenceAdmin(admin.ModelAdmin):
    pass
