from django.urls import path, include
from .views import StartupProfileViews, StartupPositionViews
from . import views


urlpatterns = [
    path('get_startup_profile/<str:username>/', StartupProfileViews.get_startup_profile, name='get-startup-profile'),
    path('update_startup_profile/', StartupProfileViews.update_startup_profile, name='update-startup-profile'),
    path("position/create/", StartupPositionViews.create_startup_position, name="create_startup_position"),
    path("profile/<int:startup_profile_id>/team/", include("team.urls")),
    path("profile/<int:startup_profile_id>/vote/", views.VoteProfile.as_view(), name="like-profile"),
    path("position/update/<int:position_id>/", StartupPositionViews.update_startup_position, name="update_startup_position"),
]