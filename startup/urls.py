from django.urls import path
from .views import StartupProfileViews, StartupPositionViews
from django.urls import include, path

urlpatterns = [
    path('get_startup_profile/<str:username>/', StartupProfileViews.get_startup_profile, name='get-startup-profile'),
    path('update_startup_profile/', StartupProfileViews.update_startup_profile, name='update-startup-profile'),
    path("position/create/", StartupPositionViews.create_startup_position, name="create_startup_position"),
    path("position/update/<int:position_id>/", StartupPositionViews.update_startup_position, name="update_startup_position"),
    path("position/delete/<int:position_id>/", StartupPositionViews.delete_startup_position, name="delete_startup_position"),
    path("profile/<int:startup_profile_id>/team/", include("team.urls")),

]
