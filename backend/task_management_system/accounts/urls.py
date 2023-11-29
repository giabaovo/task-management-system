from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.api import (
    AccountRegister, 
    AccountVerify, 
    ResendAccountVerifyEmail,
    ForgotPassword,
    ForgotPasswordVerify,
    ResetPassword
)

urlpatterns = [
    path("forgot_password/", ForgotPassword.as_view(), name="forgot_password"),
    path("forgot_password_verify/", ForgotPasswordVerify.as_view(), name="forgot_password_verify"),
    path("reset_password/", ResetPassword.as_view(), name="reset_password"),

    path("resend/", ResendAccountVerifyEmail.as_view(), name="resend"),
    path("verify/", AccountVerify.as_view(), name="account_verify"),
    path("register/", AccountRegister.as_view(), name="register"),

    #API View for get access and refresh token from user credentials
    path("login/", TokenObtainPairView.as_view(), name="login"),

    #API View for get new access token from refresh token
    path("login/refresh/", TokenRefreshView.as_view(), name="login_refresh"),
]
