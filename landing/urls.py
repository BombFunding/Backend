from django.urls import path
from . import views

urlpatterns = [
    path('top_liked_startups/', views.top_liked_startups, name='top-visited-startups'),
    path('top_visited_startups/', views.top_visited_startups, name='top-visited-startups'),
    path('top_funded_startups/', views.top_funded_startups, name='top_funded_startups'),
    path('get_statistics/', views.get_statistics, name='get_statistics'),
]

