from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ForgetPasswordEmailView,
    LoginView,
    RegisterView,
    ResetPasswordView,
    change_user_password
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", include("django_email_verification.urls")),
    path("forgetpassword/", ForgetPasswordEmailView.as_view(), name="password_reset"),
    path("resetpassword/", ResetPasswordView.as_view(), name="password_reset_confirm"),
    path("change_password/", change_user_password, name="change_user_password"),
]
