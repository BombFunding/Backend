from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ForgetPasswordEmailView,
    LoginView,
    RegisterView,
    ResetPasswordView,
    change_user_password,
    view_own_baseuser_profile,
    update_baseuser_profile,
    baseuser_search_by_name,
    add_comment,
    get_comments_by_profile,
    edit_comment,
    delete_comment
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", include("django_email_verification.urls")),
    path("forgetpassword/", ForgetPasswordEmailView.as_view(), name="password_reset"),
    path("resetpassword/", ResetPasswordView.as_view(), name="password_reset_confirm"),
    path("change_password/", change_user_password, name="change_user_password"),
    path(
        "update_baseuser_profile/", update_baseuser_profile, name="update_baseuser_profile"
    ),
    path(
        "baseuser_search_by_name/<str:username>/",
        baseuser_search_by_name,
        name="baseuser_search_by_name",
    ),
    path(
        "view_own_baseuser_profile/",
        view_own_baseuser_profile,
        name="view_own_baseuser_profile",
    ),
    # path("comment_on_profile/<str:username>/", add_comment, name="add_comment"),
    # path(
    # "all_comments_of_profile/<str:username>/",
    # get_comments_by_profile,
    # name="get_comments_by_profile",
    # ),
    # path(
    #     "delete_comment/<int:comment_id>/", delete_comment, name="delete_comment"
    # ),
    # path("edit_comment/<int:comment_id>/", edit_comment, name="edit_comment"),
]
