from django.urls import path
from .views import WeeklyStatsView

urlpatterns = [
    path('weekly-stats/', WeeklyStatsView.as_view(), name='weekly-stats'),
]
