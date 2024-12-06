from django.urls import path
from . import views

urlpatterns = [
    path('top-visited-startups/', views.top_visited_startups, name='top-visited-startups'),
    # path('top-funded-startups/', views.top_funded_startups, name='top_funded_startups'),
]

