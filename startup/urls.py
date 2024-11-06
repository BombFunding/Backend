from django.urls import path
from . import views

urlpatterns = [
    path('startup-profile/', views.startup_profile, name='startup-profile'),
    path('create-update-position/', views.create_update_position, name='create_update_position'),

]