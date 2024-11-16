import datetime

from django.db.models import F
from django.core.exceptions import FieldError
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from alert_system.utils import convert_to_decimal, convert_to_boolean
from health_alert.models.health_measurement_models import EmployeeHealthMeasurement
from health_alert.models.health_reference_models import EmployeeHealthReference
from health_alert.serializers import EmployeeHealthReferenceSerializer, EmployeeHealthMeasurementSerializer, \
    EmployeeHealthMeasurementGraphSerializer
from alert_system.statuses import SwaggerStatuses
from organization.models import Employee


class EmployeeHealthReferenceView(generics.GenericAPIView):
    serializer_class = EmployeeHealthReferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        employee_id = self.kwargs.get("pk")
        get_object_or_404(Employee, pk=employee_id)
        queryset = EmployeeHealthReference.objects.filter(
            employee=employee_id
        )
        return queryset

    @extend_schema(
        tags=["Health alert"],
        summary="Get employee's health reference",
        responses={
            status.HTTP_200_OK: EmployeeHealthReferenceSerializer,
            **SwaggerStatuses.SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES,
        }
    )
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["Health alert"],
        summary="Create employee's health reference",
        examples=[
            OpenApiExample(
                name='Create a new employee health reference',
                value={
                    "blood_group": 1,
                    "rhesus_factor": "True",
                    "normal_systolic_pressure": 120,
                    "normal_diastolic_pressure": 80,
                    "normal_pulse": 60,
                    "normal_temperature": 36.5,
                    "normal_steps": 5000,
                    "normal_stress_level": 50,
                    "normal_oxygen_level": 95
                },
                request_only=True
            ),
        ],
        responses={
            status.HTTP_201_CREATED: status.HTTP_201_CREATED,
            **SwaggerStatuses.SCHEMA_RETRIEVE_UPDATE_DESTROY_STATUSES,
        }
    )
    def post(self, request, *args, **kwargs):
        employee_id = kwargs.get("pk")
        employee = get_object_or_404(Employee, pk=employee_id)

        try:
            employee_health_reference = EmployeeHealthReference.objects.get(employee=employee)
            employee_health_reference.delete()
        except EmployeeHealthReference.DoesNotExist:
            pass

        health_reference_data = {
            "normal_systolic_pressure": request.data.get("normal_systolic_pressure"),
            "normal_diastolic_pressure": request.data.get("normal_diastolic_pressure"),
            "normal_pulse": request.data.get("normal_pulse"),
            "normal_temperature": request.data.get("normal_temperature"),
            "normal_stress_level": request.data.get("normal_stress_level"),
            "normal_oxygen_level": request.data.get("normal_oxygen_level"),
        }

        blood_group = request.data.get("blood_group")
        rhesus_factor = request.data.get("rhesus_factor")
        normal_steps = request.data.get("normal_steps")

        error = self.validate_input_params(health_reference_data, blood_group, rhesus_factor, normal_steps)
        if error:
            return error

        health_reference_data["employee"] = employee

        EmployeeHealthReference.objects.create(**health_reference_data)
        return Response(status=status.HTTP_201_CREATED)

    def validate_input_params(self, health_reference_data, blood_group, rhesus_factor, normal_steps):
        for key, value in health_reference_data.items():
            value = convert_to_decimal(value)
            if isinstance(value, dict):
                return Response(data=value, status=status.HTTP_400_BAD_REQUEST)
            health_reference_data[key] = value

        try:
            health_reference_data["blood_group"] = int(blood_group)
            health_reference_data["rhesus_factor"] = convert_to_boolean(rhesus_factor.lower())
            health_reference_data["normal_steps"] = int(normal_steps)
        except (ValueError, TypeError):
            error = {"detail": "Invalid value"}
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=health_reference_data)
        serializer.is_valid(raise_exception=True)
        return None


class EmployeeHealthMeasurementView(generics.GenericAPIView):
    serializer_class = EmployeeHealthMeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        employee_id = self.kwargs.get("pk")
        get_object_or_404(Employee, pk=employee_id)
        queryset = EmployeeHealthMeasurement.objects.filter(
            employee=employee_id
        ).order_by("-last_update")[:1]
        return queryset

    @extend_schema(
        tags=["Health alert"],
        summary="Get employee's health measurement",
        responses={
            status.HTTP_200_OK: EmployeeHealthReferenceSerializer,
            **SwaggerStatuses.SCHEMA_GET_POST_STATUSES,
        }
    )
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)


class EmployeeHealthMeasurementGraphView(generics.GenericAPIView):
    serializer_class = EmployeeHealthMeasurementGraphSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        employee_id = self.kwargs.get("pk")
        get_object_or_404(Employee, pk=employee_id)
        queryset = EmployeeHealthMeasurement.objects.filter(
            employee=employee_id
        ).order_by("-last_update")
        return queryset

    @extend_schema(
        tags=["Health alert"],
        summary="Get data for graph of employee's health measurement",
        parameters=[
            OpenApiParameter(
                name="health_indicator",
                type={"type": "string"},
                description="Health indicator:",
                required=True,
                enum=[
                    "systolic_pressure",
                    "diastolic_pressure",
                    "pulse",
                    "temperature",
                    "steps",
                    "stress_level",
                    "oxygen_level"
                ],
            )
        ],
        description="Get data for current day for graph of employee's health measurement",
        responses={
            status.HTTP_200_OK: EmployeeHealthMeasurementGraphSerializer,
            **SwaggerStatuses.SCHEMA_GET_POST_STATUSES,
        }
    )
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        error, qs = self.filter_queryset(qs)
        if error:
            return error
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    def filter_queryset(self, qs):
        health_indicator = self.request.query_params.get("health_indicator")
        today_date = datetime.date.today()
        try:
            qs = qs.filter(
                last_update__date=today_date
            ).values(
                "last_update", health_value=F(health_indicator)
            )
        except FieldError:
            error = {"detail": "Invalid health indicator"}
            error = Response(data=error, status=status.HTTP_400_BAD_REQUEST)
            return error, None
        return None, qs