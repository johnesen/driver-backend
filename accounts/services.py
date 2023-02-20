import random
from typing import Tuple

from django.conf import settings
from django.db.models import QuerySet
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate

from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from common.exceptions import *
from common.message import my_message
from common.validators import validate_user_password

from accounts.models import User, DriverProfile, ClientProfile
from accounts.settings import PHONE_RE, MAIL_RE, UserTypes


class TokenService:
    token = RefreshToken

    @classmethod
    def create_auth_token_by_login_password(
        cls, login: str, password: str
    ) -> Tuple[User, RefreshToken, RefreshToken]:
        user = authenticate(username=login, password=password)
        if user:
            token = cls.token.for_user(user)
            return user, token
        else:
            raise ObjectNotFoundException(
                "User not found or not active or data is not valid"
            )

    @classmethod
    def create_auth_token_by_user(cls, user: QuerySet) -> dict:
        token = cls.token.for_user(user)
        return user, token


class UserService:
    __model = User
    __driver_model = DriverProfile
    __client_model = ClientProfile

    @classmethod
    def get(cls, **filters) -> User:
        return cls.__model.objects.get(**filters)

    @classmethod
    def get_user(cls, **filters) -> User:
        try:
            return cls.__model.objects.get(**filters)
        except cls.__model.DoesNotExist:
            raise ObjectNotFoundException("User not found")

    @classmethod
    def filter_user(cls, **filters):
        return cls.__model.objects.filter(**filters)

    @classmethod
    def exclude_user(cls, **filters):
        return cls.__model.objects.exclude(**filters)

    @classmethod
    def create_user_with_code(
        cls,
        login: str,
        password: str,
        conf_password: str,
        user_type: str,
    ) -> User:
        if not MAIL_RE.match(login):
            raise exceptions.NotAcceptable(detail="not valid email")
        if cls.__model.objects.filter(login=login).exists():
            raise UserAlreadyExist("User with this email alredy exists")
        correct_password = validate_user_password(
            password=password, conf_password=conf_password
        )
        user = cls.__model(email=login, login=login)
        user.code = SendCodeService.send_email(email=login)
        user.set_password(correct_password)
        user.save()
        if user_type == UserTypes.driver:
            user.is_driver = True
            user.save()
            cls.__driver_model.objects.create(user=user)
        if user_type == UserTypes.client:
            user.is_client = True
            user.save()
            cls.__client_model.objects.create(user=user)
        return user

    @classmethod
    def resend_code(cls, login: str, for_reset=False):
        if not MAIL_RE.match(login):
            raise exceptions.NotAcceptable(detail="not valid email")
        if cls.__model.objects.filter(login=login).exists():
            user = cls.__model.objects.get(login=login)
            new_activation_code = SendCodeService.send_email(login, for_reset)
            user.code = new_activation_code
            user.save()
        else:
            raise ObjectNotFoundException("User with this email was not found")
        
    
    @classmethod
    def change_password_user(
        cls, user: User, old_psw: str, new_psw: str, conf_new_psw: str
    ) -> User:
        user = cls.get_user(id=user.pk)
        if not user.check_password(raw_password=old_psw):
            raise IncorrectPasswordException("The current password is not correct")
        correct_new_password = validate_user_password(
            password=new_psw, conf_password=conf_new_psw
        )
        user.set_password(correct_new_password)
        user.save()
        return user

    @classmethod
    def check_code_and_update_password(
        cls, code: int, new_password: str, confirm_new_password: str
    ):
        try:
            code = int(code)
            if new_password == confirm_new_password:
                if cls.__model.objects.filter(code=code).exists():
                    user = cls.__model.objects.get(code=code)
                    if user.is_active:
                        user.code = None
                        user.set_password(new_password)
                        user.save()
                        return user
                    else:
                        raise ObjectNotFoundException("User is not activated")
                else:
                    raise IncorrectCodeException("Incorrect activation code")
            else:
                raise IncorrectPasswordException("Password mismatch")
        except ValueError:
            raise TypeErrorException("The code must be numeric")

class SendCodeService:
    __model = User

    @classmethod
    def activate_user(cls, code: str):
        try:
            code = int(code)
            if cls.__model.objects.filter(code=code):
                user = cls.__model.objects.get(code=code)
                user.is_active = True
                user.code = None
                user.save()
                return user
            else:
                raise IncorrectCodeException(
                    "Incorrect values or user has been activated"
                )
        except ValueError:
            raise TypeErrorException("The code must be numeric")

    @classmethod
    def check_code(cls, code: str):
        try:
            code = int(code)
            if cls.__model.objects.filter(code=code):
                user = cls.__model.objects.get(code=code)
                return user
            else:
                raise IncorrectCodeException(
                    "Incorrect values or user has been activated"
                )
        except ValueError:
            raise TypeErrorException("The code must be numeric")

    @staticmethod
    def create_code():
        activation_code = str(random.randint(100000, 999999))
        return activation_code

    @classmethod
    def create_activation_code(cls, login: str):
        activation_code = cls.create_code()
        if not cls.__model.objects.filter(code=activation_code).exists():
            return activation_code
        else:
            return cls.create_activation_code(login)

    @classmethod
    def send_email(cls, email, for_reset=False):
        activation_code = cls.create_activation_code(email)
        data = my_message(activation_code, for_reset)
        email = EmailMessage(subject=data["subject"], body=data["body"], to=[email])
        email.send()
        return activation_code
