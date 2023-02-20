from django.urls import path, include
from accounts import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("resend-code/", views.ResendCodeAPIView.as_view(), name="resend-code"),
    path("activate/", views.ActivateUserAPIView.as_view(), name="activate"),
    path("refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", views.ProfileApiView.as_view(), name="profile"),
    path('passwords/changes/', views.ChangePasswordAPIView.as_view(), name='post-change-password'),
    path('passwords/send-code/', views.SendCodeForResetPasswordAPIView.as_view(), name='send-password'),
    path('passwords/check-code/', views.CheckCodeForPasswordResetUserAPIView.as_view(), name='check-send-password'),
    path('passwords/reset-password/', views.ConfirmNewPasswordAPIView.as_view(), name='update-password'),
]
