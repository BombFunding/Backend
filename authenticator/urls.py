from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ForgetPasswordEmailView,
    LoginView,
    RegisterView,
    ResetPasswordView,
    ChangeUserPasswordView,
    UpdateBasicUserProfileView,
    ViewBasicUserProfileView,
    ViewOwnBasicUserProfileView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", include("django_email_verification.urls")),
    path("forgetpassword/", ForgetPasswordEmailView.as_view(), name="password_reset"),
    path("resetpassword/", ResetPasswordView.as_view(), name="password_reset_confirm"),
    path("profile/", ViewOwnBasicUserProfileView.as_view(), name="view_own_basic_user_profile"),
    path(
        "profile/<str:username>/",
        ViewBasicUserProfileView.as_view(),
        name="view_basic_user_profile",
    ),
    path(
        "update_basic_user_profile/",
        UpdateBasicUserProfileView.as_view(),
        name="update_basic_user_profile",
    ),
    path("change_password/", ChangeUserPasswordView.as_view(), name="change_user_password"),
]
