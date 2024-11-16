from django.contrib.postgres.search import SearchVector, SearchQuery
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework import generics, status, permissions

from alert_system.statuses import SwaggerStatuses

from organization.models import Employee
from organization.serializers import EmployeeSerializer, EmployeesListSerializer, CreateEmployeeSerializer


class EmployeesView(generics.ListCreateAPIView):
    queryset = Employee.objects.exclude(
        is_staff=True,
        is_superuser=True
    ).order_by(
        "current_status"
    ).order_by(
        "last_name"
    )
    serializer_class = EmployeesListSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Employee"],
        summary="Get all employees",
        parameters=[
            OpenApiParameter(
                name="search",
                type={"type": "string"},
                description="Search parameter",
                required=False,
            )
        ],
        responses={
            status.HTTP_200_OK: EmployeeSerializer(many=True),
            **SwaggerStatuses.SCHEMA_GET_POST_STATUSES,
        }
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        search = self.request.query_params.get('search')
        if search:

            search_vector = SearchVector(
                'first_name',
                'last_name',
                'middle_name',
                'position'
            )
            search_query = SearchQuery(search)

            queryset = queryset.annotate(
                search=search_vector
            ).filter(
                search=search_query
            )

        return queryset

    @extend_schema(
        tags=["Employee"],
        summary="Create employee",
        examples=[
            OpenApiExample(
                name='Create a new employee',
                value={
                    "first_name": "Erich",
                    "last_name": "Remarque",
                    "middle_name": "Maria",
                    "birth_date": "1898-06-11",
                    "gender": "MALE",
                    "current_status": "2_NORMAL",
                    "phone_number": "+7(930) 123-45-67",
                    "position": "writer",
                    "username": "erich_remarque",
                    "password": "some_password",
                    "email": "erich_remarque@gmail.com",
                },
                request_only=True
            ),
        ],
        responses={
            status.HTTP_201_CREATED: status.HTTP_201_CREATED,
            **SwaggerStatuses.SCHEMA_GET_POST_STATUSES,
        }
    )
    def post(self, request, *args, **kwargs):
        self.serializer_class = CreateEmployeeSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class EmployeeView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Employee"],
        summary="Get employee by id",
        responses={
            status.HTTP_200_OK: EmployeeSerializer,
            **SwaggerStatuses.SCHEMA_GET_POST_STATUSES,
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
