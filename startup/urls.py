from django.urls import path

from . import views

urlpatterns = [
    path('get_startup_profile/<str:username>/', views.get_startup_profile, name='get-startup-profile'),
    path('update_startup_profile/', views.update_startup_profile, name='update-startup-profile'),
    path("position/create/", views.create_startup_position, name="create_startup_position"),
    path("position/update/<int:position_id>/", views.update_startup_position, name="update_startup_position"),
]
