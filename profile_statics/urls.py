from django.urls import path
from .views import ProfileStaticsLast7DaysView
from .views import ProfileStaticsLast6MonthsView
from .views import CheckProfileLikeView

urlpatterns = [
    path('last-7-days/', ProfileStaticsLast7DaysView.as_view(), name='profile-statistics-last-7-days'),
    path('last-6-months/', ProfileStaticsLast6MonthsView.as_view(), name='profile-statistics-last-6-months'),
    path('check-like/', CheckProfileLikeView.as_view(), name='check-profile-like'),
]