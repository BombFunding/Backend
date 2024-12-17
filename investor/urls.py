from django.urls import path
from .views import InvestorProfileUpdateView

urlpatterns = [
    path("investor/update/<int:pk>/", InvestorProfileUpdateView.as_view(), name="investor-update"),
]
