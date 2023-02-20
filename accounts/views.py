from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions

from common.schemas.accounts import *

from accounts.serializers import *
from accounts.services import *

# from accounts.mixins import FilterOrderHistoryByQueryParamsMixin
from accounts.serializers import UserSerializer


class RegisterAPIView(generics.CreateAPIView):

    permission_classes = [permissions.AllowAny]
    schema = UserRegisterSchema()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        data = UserService.create_user_with_code(
            login=serializer.validated_data.get("login"),
            password=serializer.validated_data.get("password"),
            conf_password=serializer.validated_data.get("confirm_password"),
            user_type=serializer.validated_data.get("user_type"),
        )
        return Response(
            data={
                "message": "The user has been successfully created. Check your email you should get a code",
                "status": "registered",
                "login": str(data),
            },
            status=status.HTTP_201_CREATED,
        )


class ResendCodeAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    schema = SendCodeForResetPasswordSchema()
    serializer_class = ResendActivationCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserService.resend_code(
            login=serializer.validated_data.get("login"),
        )

        return Response(
            data={
                "message": "Code was succesfully resended",
                "status": "resended",
            },
            status=status.HTTP_200_OK,
        )


class ActivateUserAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    schema = ActivationUserSchema()
    serializer_class = UserActivateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        activated = SendCodeService.activate_user(
            code=serializer.validated_data.get("code")
        )
        user, token = TokenService.create_auth_token_by_user(activated)

        return Response(
            data={
                "message": "Account has been successfully activated",
                "status": "activated",
                "data": {
                    "refresh_token": str(token),
                    "access_token": str(token.access_token),
                    "token_type": "Bearer",
                    "user": UserSerializer(user).data,
                },
                "token_type": "Bearer",
            },
            status=status.HTTP_200_OK,
        )


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    schema = LoginSchema()

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = TokenService.create_auth_token_by_login_password(
            login=serializer.validated_data.get("login"),
            password=serializer.validated_data.get("password"),
        )
        return Response(
            data={
                "message": "You have successfully logged in",
                "data": {
                    "refresh_token": str(token),
                    "access_token": str(token.access_token),
                    "token_type": "Bearer",
                    "user": UserSerializer(user).data,
                },
                "status": "logged",
            },
            status=status.HTTP_200_OK,
        )


class ProfileApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    pagination_class = None
    schema = ProfileSchema()

    def get(self, request):
        return Response(
            data={
                "message": "User profile data was succesfully retrieved",
                "data": UserSerializer(request.user).data,
                "status": "retrieved-pofile",
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data={
                    "message": "User profile data was succesfully updated(patched)",
                    "data": UserSerializer(request.user).data,
                    "status": "updated-pofile",
                },
                status=status.HTTP_202_ACCEPTED,
            )


class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    schema = ChangePasswordSchema()

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserService.change_password_user(
            user=request.user,
            old_psw=serializer.validated_data.get("old_password"),
            new_psw=serializer.validated_data.get("new_password"),
            conf_new_psw=serializer.validated_data.get("confirm_new_password"),
        )
        return Response(
            data={
                "message": "The password has been successfully changed",
                "status": "OK",
            },
            status=status.HTTP_200_OK,
        )


class SendCodeForResetPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    schema = SendCodeForResetPasswordSchema()

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserService.resend_code(
            login=serializer.validated_data.get("login"), for_reset=True
        )
        return Response(
            data={
                "message": "The code was sent successfully",
                "status": "reset_code_sended",
            },
            status=status.HTTP_200_OK,
        )


class CheckCodeForPasswordResetUserAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    schema = ActivationUserSchema()
    serializer_class = UserActivateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = SendCodeService.check_code(code=serializer.validated_data.get("code"))

        return Response(
            data={
                "message": "The code is valid, go ahead fool!",
                "data": str(data),
                "status": "reset_code_ok",
            },
            status=status.HTTP_200_OK,
        )


class ConfirmNewPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    schema = ConfirmNewPasswordSchema()

    def post(self, request):
        serializer = CheckActivationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.check_code_and_update_password(
            code=serializer.validated_data.get("code"),
            new_password=serializer.validated_data.get("new_password"),
            confirm_new_password=serializer.validated_data.get("confirm_new_password"),
        )
        user, token = TokenService.create_auth_token_by_user(user)
        return Response(
            data={
                "message": "Password reset successfully",
                "data": {
                    "refresh_token": str(token),
                    "access_token": str(token.access_token),
                    "token_type": "Bearer",
                    "user": UserSerializer(user).data,
                },
                "status": "updated_password",
            },
            status=status.HTTP_200_OK,
        )
