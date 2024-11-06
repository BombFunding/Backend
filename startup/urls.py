from django.urls import path
from . import views

urlpatterns = [
    path('create-startup/', views.create_startup, name='create-startup'),
]
