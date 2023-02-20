import coreapi
from rest_framework.schemas.coreapi import AutoSchema
import coreschema


class UserRegisterSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        api_fields = []
        if method == "POST":
            api_fields = [
                coreapi.Field(
                    name="login",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="login"),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="str"),
                ),
                coreapi.Field(
                    name="confirm_password",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="str"),
                ),
            ]
        return self._manual_fields + api_fields


class LoginSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        api_fields = []
        if method == "POST":
            api_fields = [
                coreapi.Field(
                    name="login",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="email"),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="str"),
                ),
            ]
        return self._manual_fields + api_fields


class ActivationUserSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        api_fields = []
        if method == "POST":
            api_fields = [
                coreapi.Field(
                    name="code",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="positive int"),
                )
            ]
        return self._manual_fields + api_fields


class SocialLoginSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        api_fields = []
        if method == "POST":
            api_fields = [
                coreapi.Field(
                    name="token",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="id token from google"),
                ),
                coreapi.Field(
                    name="role",
                    required=False,
                    location="form",
                    schema=coreschema.String(
                        description="str(Потребитель) или str(Магазин)"
                    ),
                ),
            ]
        return self._manual_fields + api_fields


class ProfileSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        api_fields = []
        if method == "PATCH":
            api_fields = [
                coreapi.Field(
                    name="email",
                    required=False,
                    location="form",
                    schema=coreschema.String(description="email"),
                ),
                coreapi.Field(
                    name="first_name",
                    required=False,
                    location="form",
                    schema=coreschema.String(description="str(ФИО)"),
                ),
                coreapi.Field(
                    name="middle_name",
                    required=False,
                    location="form",
                    schema=coreschema.String(description="str(ФИО)"),
                ),
                coreapi.Field(
                    name="last_name",
                    required=False,
                    location="form",
                    schema=coreschema.String(description="str(ФИО)"),
                ),
                coreapi.Field(
                    name="phone",
                    required=False,
                    location="form",
                    schema=coreschema.String(description="+996*********"),
                ),
                coreapi.Field(
                    name="photo",
                    required=False,
                    location="form",
                    schema=coreschema.String(description="file"),
                ),
            ]

        return self._manual_fields + api_fields


class ChangePasswordSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        api_fields = []
        if method == "POST":
            api_fields = [
                coreapi.Field(
                    name="old_password",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="str"),
                ),
                coreapi.Field(
                    name="new_password",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="str"),
                ),
                coreapi.Field(
                    name="confirm_new_password",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="str"),
                ),
            ]
        return self._manual_fields + api_fields


class SendCodeForResetPasswordSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        api_fields = []
        if method == "POST":
            api_fields = [
                coreapi.Field(
                    name="login",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        description="login (email or phone number)"
                    ),
                )
            ]
        return self._manual_fields + api_fields


class ConfirmNewPasswordSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        api_fields = []
        if method == "POST":
            api_fields = [
                coreapi.Field(
                    name="code",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="int"),
                ),
                coreapi.Field(
                    name="new_password",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="str"),
                ),
                coreapi.Field(
                    name="confirm_new_password",
                    required=True,
                    location="form",
                    schema=coreschema.String(description="str"),
                ),
            ]
        return self._manual_fields + api_fields


class OrderHistorySchema(AutoSchema):
    def get_manual_fields(self, path, method):
        api_fields = []
        if method == "GET":
            api_fields = [
                coreapi.Field(
                    name="payment_method",
                    required=False,
                    location="query",
                    schema=coreschema.String(
                        description="payment method (Картой, Наличными)"
                    ),
                ),
                coreapi.Field(
                    name="status",
                    required=False,
                    location="query",
                    schema=coreschema.String(
                        description="status (Новая заявка, В обработке, Завершена, Отклонена)"
                    ),
                ),
                coreapi.Field(
                    name="start",
                    required=False,
                    location="query",
                    schema=coreschema.String(
                        description="filter by date, date_format: DD-MM-YY"
                    ),
                ),
                coreapi.Field(
                    name="end",
                    required=False,
                    location="query",
                    schema=coreschema.String(
                        description="filter by date, date_format: DD-MM-YY"
                    ),
                ),
            ]
        return self._manual_fields + api_fields
