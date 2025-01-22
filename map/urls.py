
from django.urls import path
from . import views

urlpatterns = [
    path('pins/', views.PinListView.as_view(), name='pin-list'),
    path('pins/add/', views.PinCreateView.as_view(), name='pin-create'),
]
