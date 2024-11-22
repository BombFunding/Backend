from django.urls import path, include
from .views import RegisterView, LoginView, ForgetPasswordEmailView, ResetPasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", include("django_email_verification.urls")),
    path("forgetpassword/", ForgetPasswordEmailView.as_view(), name="password_reset"),
    path("resetpassword/", ResetPasswordView.as_view(), name="password_reset_confirm"),

]
