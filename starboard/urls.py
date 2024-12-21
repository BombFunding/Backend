from django.urls import path
from . import views  

urlpatterns = [
    path('top-startups/', views.get_top_startups, name='top_startups'),  
]

# example with curl
# curl -X GET "http://127.0.0.1:8000/starboard/top-startups/?filter_by_subcategory=%5B%22software%22%5D&type=top_liked"
