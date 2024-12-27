from django.urls import path
from .views import (
    ProjectStatisticsLast6MonthsView,
    ProjectStatisticsLast7DaysView,
    ProjectVisitView,
    ProjectVisitCountView,
    StartupVisitCountView,
)

urlpatterns = [
    path('last-7-days/', ProjectStatisticsLast7DaysView.as_view(), name='profile-statistics-last-7-days'),
    path('last-6-months/', ProjectStatisticsLast6MonthsView.as_view(), name='profile-statistics-last-6-months'),
    path('visit/<int:project_id>/', ProjectVisitView.as_view(), name='project-visit'),
    path('visit/project/<int:project_id>/', ProjectVisitCountView.as_view(), name='project-visit-count'),
    path('visit/startup/<int:startup_id>/', StartupVisitCountView.as_view(), name='startup-visit-count'),
]
