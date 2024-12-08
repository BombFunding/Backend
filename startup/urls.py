from django.urls import path, include
from .views import StartupProfileRetrieveView, StartupProfileUpdateView, StartupPositionCreateView, StartupPositionUpdateView, StartupPositionDeleteView , VoteProfile

urlpatterns = [
    path('get_startup_profile/<str:username>/', StartupProfileRetrieveView.as_view(), name='get-startup-profile'),
    path('update_startup_profile/', StartupProfileUpdateView.as_view(), name='update-startup-profile'),
    path("position/create/", StartupPositionCreateView.as_view(), name="create_startup_position"),
    path("position/update/<int:position_id>/", StartupPositionUpdateView.as_view(), name="update_startup_position"),
    path("position/delete/<int:position_id>/", StartupPositionDeleteView.as_view(), name="delete_startup_position"),
    path("profile/<int:startup_profile_id>/team/", include("team.urls")),
    path("profile/<int:startup_profile_id>/vote/", VoteProfile.as_view(), name="like-profile"),
]
