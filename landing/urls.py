from django.urls import path
from . import views

urlpatterns = [
    path('top_liked_startups/', views.top_liked_startups, name='top-visited-startups'),
    path('top_visited_startups/', views.top_visited_startups, name='top-visited-startups'),
    path('top_funded_startups/', views.top_funded_startups, name='top_funded_startups'),
    path('get_statistics/', views.get_statistics, name='get_statistics'),
    path('category-revenue/', views.CategoryFunded, name='category_revenue'),
    path('category-count/', views.CategoryUserCount, name='category-count'),
    path('category-viewd/', views.CategoryViewd, name='category-viewd'),
    path('category-liked/', views.CategoryLiked, name='category-liked'),
    path('total-funded/', views.total_funded_positions, name='total-funded'),
]
