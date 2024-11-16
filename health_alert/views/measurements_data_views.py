from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from alert_system.utils import convert_to_decimal
from health_alert.models.health_measurement_models import EmployeeHealthMeasurement
from health_alert.serializers import UploadDataSerializer
from alert_system.statuses import SwaggerStatuses
from organization.models import Employee


class UploadDataView(generics.GenericAPIView):
    serializer_class = UploadDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Measurements"],
        summary="Upload data for employee's health measurement",
        examples=[
            OpenApiExample(
                name="Example of upload data health measurement",
                value={
                    "systolic_pressure": 120,
                    "diastolic_pressure": 80,
                    "pulse": 60,
                    "temperature": 36.5,
                    "steps": 5000,
                    "stress_level": 50,
                    "oxygen_level": 95,
                    "latitude": 0.0,
                    "longitude": 0.0
                },
                request_only=True
            ),
        ],
        responses={
            status.HTTP_201_CREATED: status.HTTP_201_CREATED,
            **SwaggerStatuses.SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES,
        },
    )
    def post(self, request, *args, **kwargs):
        employee_id = kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=employee_id)

        health_measurement_data = {
            "systolic_pressure": request.data.get("systolic_pressure"),
            "diastolic_pressure": request.data.get("diastolic_pressure"),
            "pulse": request.data.get("pulse"),
            "temperature": request.data.get("temperature"),
            "stress_level": request.data.get("stress_level"),
            "oxygen_level": request.data.get("oxygen_level"),
            "latitude": request.data.get("latitude"),
            "longitude": request.data.get("longitude"),
        }
        steps = request.data.get("steps")
        error = self.validate_input_params(health_measurement_data, steps)
        if error:
            return error

        health_measurement_data["employee"] = employee

        EmployeeHealthMeasurement.objects.create(**health_measurement_data)
        return Response(status=status.HTTP_201_CREATED)

    def validate_input_params(self, health_measurement_data, steps):
        for key, value in health_measurement_data.items():
            value = convert_to_decimal(value)
            if isinstance(value, dict):
                return Response(data=value, status=status.HTTP_400_BAD_REQUEST)
            health_measurement_data[key] = value

        try:
            health_measurement_data["steps"] = int(str(steps))
        except (ValueError, TypeError):
            error = {"detail": "Invalid value"}
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=health_measurement_data)
        serializer.is_valid(raise_exception=True)
        return None
