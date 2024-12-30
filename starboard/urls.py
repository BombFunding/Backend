from django.urls import path
from . import views  

urlpatterns = [
    path('top-visited/', views.top_visited_projects, name='top_visited_projects'),
    path('top-liked/', views.top_liked_projects, name='top_liked_projects'),
    path('most-recent/', views.most_recent_projects, name='most_recent_projects'),
]

# example with curl
# curl -X GET "http://127.0.0.1:8000/starboard/top-startups/?filter_by_subcategory=%5B%22software%22%5D&type=top_liked"
