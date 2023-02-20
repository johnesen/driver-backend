from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel

from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    login = models.CharField(
        max_length=250, unique=True, verbose_name=_("Логин"), null=True, blank=True
    )
    email = models.EmailField(_("почта"), unique=True, null=True, blank=True)
    password = models.CharField(
        max_length=128, blank=True, null=True, verbose_name=_("password")
    )
    phone = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("номер телефона"),
    )
    photo = models.ImageField(
        _("фотография"), upload_to="user_media/%Y/%m/%d/", null=True, blank=True
    )
    code = models.PositiveIntegerField(
        null=True, blank=True, unique=True, verbose_name=_("код активации")
    )
    password = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_("пароль"),
    )
    first_name = models.CharField(
        blank=True, null=True, max_length=250, verbose_name=_("Имя")
    )
    last_name = models.CharField(
        blank=True, null=True, max_length=100, verbose_name=_("Фамилия")
    )
    middle_name = models.CharField(
        blank=True, null=True, max_length=100, verbose_name=_("Очество")
    )
    is_staff = models.BooleanField(default=False, verbose_name=_("Сотрудник"))
    is_superuser = models.BooleanField(default=False, verbose_name=_("Админ"))
    is_active = models.BooleanField(default=False, verbose_name=_("Активный"))
    is_driver = models.BooleanField(default=False, verbose_name=_("Водитель"))
    is_client = models.BooleanField(default=False, verbose_name=_("Клиент"))

    USERNAME_FIELD = "login"

    objects = UserManager()

    def __str__(self):
        return f"{self.login}"

    class Meta:
        db_table = "users"
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"
        ordering = ("-created_at",)


class DriverProfile(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="driver",
        verbose_name=_("Пользователь"),
    )
    about = models.CharField(
        blank=True, null=True, max_length=100, verbose_name=_("О себе")
    )
    driver_age = models.PositiveIntegerField(
        default=0, verbose_name=_("Возрасть водителя")
    )

    experience = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name=_("Стаж как водителя (years)"),
    )
    car = models.CharField(
        blank=True, null=True, max_length=100, verbose_name=_("Машина")
    )
    seats_amoutn = models.PositiveIntegerField(
        default=0, verbose_name=_("Количество мест в машине")
    )

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        db_table = "drivers"
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"
        ordering = ("-created_at",)


class DriverReviews(BaseModel):
    driver = models.ForeignKey(
        DriverProfile,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="reviews",
        verbose_name=_("Водитель"),
    )
    stars = models.PositiveSmallIntegerField(
        _("rating"),
        choices=((1, "☆"), (2, "☆ ☆"), (3, "☆ ☆ ☆"), (4, "☆ ☆ ☆ ☆"), (5, "☆ ☆ ☆ ☆ ☆")),
        null=False,
    )
    comment = models.TextField(null=True, blank=True, verbose_name=_("Отзыв"))

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        db_table = "driver_reviews"
        verbose_name = "Отзывы водителя"
        verbose_name_plural = "Отзывы водителя"
        ordering = ("-created_at",)


class ClientProfile(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="client",
        verbose_name=_("Пользователь"),
    )

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        db_table = "clients"
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ("-created_at",)
