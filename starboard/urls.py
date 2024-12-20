from django.urls import path
from . import views  

urlpatterns = [
    path('top-startups/', views.top_startups, name='top_startups'),  
]
