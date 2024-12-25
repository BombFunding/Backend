from django.urls import path

from . import views

urlpatterns = [
    path("to_startup/", views.PromotionToStartupView.as_view(), name="to_startup"),
]