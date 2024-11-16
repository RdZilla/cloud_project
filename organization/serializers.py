from rest_framework import serializers

from organization.models import Employee


class EmployeesListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    birth_date = serializers.DateField()
    gender = serializers.CharField()
    phone_number = serializers.CharField()
    position = serializers.CharField()
    current_status = serializers.CharField()

    systolic_pressure = serializers.SerializerMethodField()
    diastolic_pressure = serializers.SerializerMethodField()
    pulse = serializers.SerializerMethodField()
    temperature = serializers.SerializerMethodField()
    steps = serializers.SerializerMethodField()
    stress_level = serializers.SerializerMethodField()
    oxygen_level = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'

    @staticmethod
    def get_systolic_pressure(obj):
        measurement = obj.employeehealthmeasurement_set
        if measurement:
            systolic_pressure = measurement.order_by(
                "-last_update"
            ).values_list(
                'systolic_pressure', flat=True
            ).first()
            return systolic_pressure
        return None

    @staticmethod
    def get_diastolic_pressure(obj):
        measurement = obj.employeehealthmeasurement_set
        if measurement:
            diastolic_pressure = measurement.order_by(
                "-last_update"
            ).values_list(
                'diastolic_pressure', flat=True
            ).first()
            return diastolic_pressure
        return None

    @staticmethod
    def get_pulse(obj):
        measurement = obj.employeehealthmeasurement_set
        if measurement:
            pulse = measurement.order_by(
                "-last_update"
            ).values_list(
                'pulse', flat=True
            ).first()
            return pulse
        return None

    @staticmethod
    def get_temperature(obj):
        measurement = obj.employeehealthmeasurement_set
        if measurement:
            temperature = measurement.order_by(
                "-last_update"
            ).values_list(
                'temperature', flat=True
            ).first()
            return temperature
        return None

    @staticmethod
    def get_steps(obj):
        measurement = obj.employeehealthmeasurement_set
        if measurement:
            steps = measurement.order_by(
                "-last_update"
            ).values_list(
                'steps', flat=True
            ).first()
            return steps
        return None

    @staticmethod
    def get_stress_level(obj):
        measurement = obj.employeehealthmeasurement_set
        if measurement:
            stress_level = measurement.order_by(
                "-last_update"
            ).values_list(
                'stress_level', flat=True
            ).first()
            return stress_level
        return None

    @staticmethod
    def get_oxygen_level(obj):
        measurement = obj.employeehealthmeasurement_set
        if measurement:
            oxygen_level = measurement.order_by(
                "-last_update"
            ).values_list(
                'oxygen_level', flat=True
            ).first()
            return oxygen_level
        return None


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "id",
            "last_name",
            "first_name",
            "middle_name",
            "birth_date",
            "gender",
            "phone_number",
            "position",
        ]


class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
