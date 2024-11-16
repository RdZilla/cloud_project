from django.urls import path

from health_alert.views.health_alert_views import EmployeeHealthReferenceView, EmployeeHealthMeasurementView, \
    EmployeeHealthMeasurementGraphView
from health_alert.views.measurements_data_views import UploadDataView

urlpatterns = [
    path("employee/<str:pk>/upload_data", UploadDataView.as_view(), name="upload_data"),
    path("employee/<str:pk>/health_reference", EmployeeHealthReferenceView.as_view(),
         name="employee's health reference"),
    path("employee/<str:pk>/health_measurement", EmployeeHealthMeasurementView.as_view(),
         name="employee's health measurement"),
    path("employee/<str:pk>/health_measurement/graph", EmployeeHealthMeasurementGraphView.as_view(),
         name="data for graph of employee's health measurement"),
]
