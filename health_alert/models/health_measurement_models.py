from django.db import models

from organization.models import Employee


class EmployeeHealthMeasurement(models.Model):
    last_update = models.DateTimeField(auto_now=True, verbose_name="Дата и время последнего замера",
                                       help_text="Дата и время последнего замера умными носимыми устройствами")

    systolic_pressure = models.DecimalField(max_digits=7, decimal_places=4,
                                            verbose_name="Систолическое давление")
    diastolic_pressure = models.DecimalField(max_digits=7, decimal_places=4,
                                             verbose_name="Диастолическое давление")
    pulse = models.DecimalField(max_digits=7, decimal_places=4,
                                verbose_name="Пульс")
    temperature = models.DecimalField(max_digits=6, decimal_places=4,
                                      verbose_name="Температура")
    steps = models.IntegerField(verbose_name="Количество шагов")
    stress_level = models.DecimalField(max_digits=7, decimal_places=4,
                                       verbose_name="Уровень стресса")
    oxygen_level = models.DecimalField(max_digits=7, decimal_places=4,
                                       verbose_name="Уровень кислорода в крови")
    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   verbose_name="Широта")
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    verbose_name="Долгота")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="Сотрудник")

    def __str__(self):
        return f"Health Measurements: {self.id}"

    class Meta:
        verbose_name = "Последний замер показателей здоровья"
        verbose_name_plural = "Последние замеры показателей здоровья"
