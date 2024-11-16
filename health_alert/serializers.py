from rest_framework import serializers

from health_alert.models.health_reference_models import EmployeeHealthReference
from health_alert.models.health_measurement_models import EmployeeHealthMeasurement


class UploadDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeHealthMeasurement
        fields = "__all__"


class EmployeeHealthReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeHealthReference
        fields = '__all__'


class EmployeeHealthMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeHealthMeasurement
        fields = '__all__'


class EmployeeHealthMeasurementGraphSerializer(serializers.Serializer):
    last_update = serializers.ReadOnlyField()
    health_value = serializers.ReadOnlyField()
