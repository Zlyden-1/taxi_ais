from django.db import models

from references.models import Driver


class Rent(models.Model):
    driver = models.ForeignKey(to=Driver, on_delete=models.CASCADE, null=True, blank=False, verbose_name="Исполнитель")
    payment_date = models.DateField(null=False, blank=False, verbose_name="Дата")
    time = models.TimeField(null=True, blank=False, verbose_name="Время")
    summ = models.FloatField(null=False, blank=False, verbose_name="Сумма")
    balance = models.FloatField(null=True, blank=False, verbose_name="Баланс")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.driver} {self.payment_date}"

    class Meta:
        verbose_name_plural = "Аренда"
        verbose_name = "Аренда"
