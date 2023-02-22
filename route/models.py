from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel
from accounts.models import DriverProfile, ClientProfile


class Routes(BaseModel):
    where_from = models.CharField(
        blank=False, null=False, max_length=250, verbose_name=_("откуда")
    )
    where_to = models.CharField(
        blank=True, null=True, max_length=100, verbose_name=_("куда")
    )
    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="travels",
        verbose_name=_("Водитель"),
    )
    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=False,
        null=False,
        verbose_name=_("Цена"),
    )
    passengers = models.ManyToManyField(
        ClientProfile,
        related_name="travels",
        verbose_name=_("пассажиры")
    )
    is_open = models.BooleanField(default=False, verbose_name=_("остановки"))
    departure_date = models.DateTimeField(
        null=False, blank=False, verbose_name=_("Дата выезда")
    )
    condition = models.TextField(
        blank=True, null=True, max_length=100, verbose_name=_("условия")
    )

    def __str__(self):
        return f"{self.where_from} - {self.where_to}"

    class Meta:
        db_table = "routes"
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"
        ordering = ("-created_at",)
