from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from accounts.settings import UserTypes

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(min_length=2, required=True)
    password = serializers.CharField(min_length=2, max_length=20, required=True)


class RegisterSerializer(serializers.Serializer):
    login = serializers.CharField(
        min_length=2,
        required=True,
    )
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    user_type = serializers.ChoiceField(
        choices=UserTypes.choices(), allow_null=True, required=False
    )


class UserActivateSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6, required=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=20, required=True)
    new_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_new_password = serializers.CharField(write_only=True, required=True)


class ResetPasswordSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)


class ResendActivationCodeSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)


class CheckActivationCodeSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6, max_length=6, required=True)
    new_password = serializers.CharField(
        max_length=20, required=True, validators=[validate_password]
    )
    confirm_new_password = serializers.CharField(max_length=20, required=True)


class ConfirmPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8, max_length=20, required=True)
    confirm_new_password = serializers.CharField(
        min_length=8, max_length=20, required=True
    )


class UserSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    login = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    sign_in_method = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    middle_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    sign_in_method = serializers.CharField(read_only=True)
    photo = serializers.ImageField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)
    is_driver = serializers.BooleanField(read_only=True)
    is_client = serializers.BooleanField(read_only=True)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "phone",
            "photo",
            "is_deleted",
        ]