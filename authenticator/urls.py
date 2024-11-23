from django.urls import path, include
from .views import RegisterView, LoginView, ForgetPasswordEmailView, ResetPasswordView, view_own_basic_user_profile, view_basic_user_profile, update_basic_user_profile
from django.urls import path
from .views import RegisterView, LoginView, view_own_basic_user_profile, view_basic_user_profile, update_basic_user_profile,change_user_password
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", include("django_email_verification.urls")),
    path("forgetpassword/", ForgetPasswordEmailView.as_view(), name="password_reset"),
    path("resetpassword/", ResetPasswordView.as_view(), name="password_reset_confirm"),
    path('profile/', view_own_basic_user_profile, name='view_own_basic_user_profile'),
    path('profile/<str:username>/', view_basic_user_profile, name='view_basic_user_profile'),
    path('update_basic_user_profile/', update_basic_user_profile, name='update_basic_user_profile'),  
    path('change_password/', change_user_password, name='change_user_password'),  
]
