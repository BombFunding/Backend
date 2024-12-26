from django.urls import path, include
from .views import (
    StartupProfileRetrieveView,
    StartupProfileUpdateView,
    VoteProfile
)

import project.views

urlpatterns = [
    path('get_startup_profile/<str:username>/', StartupProfileRetrieveView.as_view(), name='get-startup-profile'),
    path('update_startup_profile/', StartupProfileUpdateView.as_view(), name='update-startup-profile'),
    path("profile/team/", include("team.urls")),
    # path("profile/<int:startup_profile_id>/vote/", VoteProfile.as_view(), name="like-profile"),
    path("projects/<str:startup_username>/", project.views.StartupProjectsList.as_view(), name="startup-projects"),
]
