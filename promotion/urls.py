from django.urls import path

from . import views

urlpatterns = [
    path("to_investor/", views.PromotionToInvestorView.as_view(), name="to_investor"),
    path("to_startup/", views.PromotionToStartupView.as_view(), name="to_startup"),
]