from django.urls import path
from .views import ProfileStaticsLast7DaysView

urlpatterns = [
    path('profile-statistics/last-7-days/', ProfileStaticsLast7DaysView.as_view(), name='profile-statistics-last-7-days'),
]
