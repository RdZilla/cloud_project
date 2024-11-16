from django.db import models

from organization.models import Employee


class EmployeeHealthReference(models.Model):
    last_update = models.DateField(auto_now=True, verbose_name="Дата контрольного замера",
                                   help_text="Дата диспансеризации и проведения контрольных замеров")

    blood_group = models.PositiveSmallIntegerField(verbose_name="Группа крови")
    rhesus_factor = models.BooleanField(verbose_name="Резус-фактор")
    normal_systolic_pressure = models.DecimalField(max_digits=7, decimal_places=4,
                                                   verbose_name="Эталонное систолическое давление")
    normal_diastolic_pressure = models.DecimalField(max_digits=7, decimal_places=4,
                                                    verbose_name="Эталонное диастолическое давление")
    normal_pulse = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="Эталонный пульс")
    normal_temperature = models.DecimalField(max_digits=6, decimal_places=4, verbose_name="Эталонная температура")
    normal_steps = models.IntegerField(verbose_name="Эталонное количество шагов")
    normal_stress_level = models.DecimalField(max_digits=7, decimal_places=4, verbose_name="Эталонный уровень стресса")
    normal_oxygen_level = models.DecimalField(max_digits=7, decimal_places=4,
                                              verbose_name="Эталонный уровень кислорода в крови")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name="Сотрудник")
    def __str__(self):
        return f"Health Benchmark: {self.id}"

    class Meta:
        verbose_name = "Эталонное значение показателей здоровья"
        verbose_name_plural = "Эталонные значения показателей здоровья"
