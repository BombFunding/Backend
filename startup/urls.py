from django.urls import path, include

from . import views

urlpatterns = [
    path(
        "create_update_position/",
        views.create_update_position,
        name="create_update_position",
    ),
    
    path('get_startup_profile/<str:username>/', views.get_startup_profile, name='get-startup-profile'),
    path("profile/<int:startup_profile_id>/team/", include("team.urls")),
    path("profile/<int:startup_profile_id>/vote/", views.VoteProfile.as_view(), name="like-profile"),
]
