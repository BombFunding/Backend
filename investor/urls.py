from django.urls import path, include
from .views import (
    InvestorProfileRetrieveView,
    InvestorProfileUpdateView,
    VoteProfile,
)

urlpatterns = [
    path('get_investor_profile/<str:username>/', InvestorProfileRetrieveView.as_view(), name='get-investor-profile'),
    path('update_investor_profile/', InvestorProfileUpdateView.as_view(), name='update-investor-profile'),
    path("profile/<int:investor_profile_id>/vote/", VoteProfile.as_view(), name="like-investor-profile"),
]