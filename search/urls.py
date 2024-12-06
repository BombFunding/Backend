from django.urls import path
from .views import BaseUserSearchView

urlpatterns = [
    path("user/", BaseUserSearchView.as_view(), name="search-user"),
]
