from django.urls import path

from . import views

urlpatterns = [
    path(
        "create_update_position/",
        views.create_update_position,
        name="create_update_position",
    ),
    
    path('get_startup_profile/<str:username>/', views.get_startup_profile, name='get-startup-profile'),
    path('update_startup_profile/', views.update_startup_profile, name='update-startup-profile'),

]
