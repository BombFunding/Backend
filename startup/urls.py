from django.urls import path, include
from .views import (
    StartupProfileRetrieveView,
    StartupProfileUpdateView,
    VoteProfile
)

urlpatterns = [
    path('get_startup_profile/<str:username>/', StartupProfileRetrieveView.as_view(), name='get-startup-profile'),
    path('update_startup_profile/', StartupProfileUpdateView.as_view(), name='update-startup-profile'),
    path("profile/team/", include("team.urls")),
    path("profile/<int:startup_profile_id>/vote/", VoteProfile.as_view(), name="like-profile"),
]
