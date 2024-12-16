from django.urls import path

from . import views

urlpatterns = [path("balance/", views.BalanceUpdateView.as_view(), name="balance")]
