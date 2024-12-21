from django.urls import path
from . import views  

urlpatterns = [
    path('top-startups/', views.get_top_startups, name='top_startups'),  
]
