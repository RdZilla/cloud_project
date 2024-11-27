from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    MALE = "MALE"
    FEMALE = "FEMALE"
    GENDER_CHOICES = (
        (MALE, "Мужской"),
        (FEMALE, "Женский")
    )

    BAD = "0_BAD"
    UNSTABLE = "1_UNSTABLE"
    NORMAL = "2_NORMAL"
    STATUS_CHOICES = (
        (BAD, "Плохой"),
        (UNSTABLE, "Нестабильный"),
        (NORMAL, "Нормальный"),
    )

    medical_metrics = {
        "systolic_pressure": {
            NORMAL: [[91, 120], [91, 120]],
            UNSTABLE: [[81, 90], [121, 139]],
            BAD: [[-float("inf"), 80], [140, float("inf")]],
        },
        "diastolic_pressure": {
            NORMAL: [[61, 80], [61, 80]],
            UNSTABLE: [[51, 60], [81, 89]],
            BAD: [[-float("inf"), 50], [90, float("inf")]],
        },
        "pulse": {
            NORMAL: [[60, 100], [60, 100]],
            UNSTABLE: [[50, 59], [101, 120]],
            BAD: [[-float("inf"), 50], [121, float("inf")]],
        },
        "temperature": {
            NORMAL: [[36.1, 37.2], [36.1, 37.2]],
            UNSTABLE: [[35.6, 36.0], [37.3, 38.0]],
            BAD: [[-float("inf"), 35.5], [38.1, float("inf")]],
        },
        "stress_level": {
            NORMAL: [[10, 39], [10, 39]],
            UNSTABLE: [[40, 69], [40, 69]],
            BAD: [[70, 100], [70, 100]],
        },
        "oxygen_level": {
            NORMAL: [[95, 100], [95, 100]],
            UNSTABLE: [[91, 94], [91, 94]],
            BAD: [[0, 90], [0, 90]],
        },
    }

    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    middle_name = models.CharField(max_length=150, verbose_name="Отчество")
    birth_date = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Пол")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона")
    position = models.CharField(max_length=150, verbose_name="Должность")
    current_status = models.CharField(max_length=150, verbose_name="Текущий статус", choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.position})"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
