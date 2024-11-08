from django.urls import path
from . import views

urlpatterns = [
    path('create-update-startup-profile/', views.create_update_startup_profile, name='startup-profile'),
    path('create-update-position/', views.create_update_position, name='create_update_position'),
    path('startup_search/<str:username>/', views.startup_search, name='get_startup_info'),
    path('search_by_date_range/', views.search_positions_by_date_range, name='search_positions_by_date_range'),  
    path('all-positions/', views.get_all_positions, name='get_all_positions'),
    path('all_startup_profiles/', views.get_all_startup_profiles, name='get_all_startup_profiles'),


    path('positions/search_by_date_range/', views.search_positions_by_date_range, name='search_positions_by_date_range'),
    path('positions/sort_by_date/', views.sort_positions_by_date, name='sort_positions_by_date'),
    path('positions/sort_by_funded/', views.sort_positions_by_funded, name='sort_positions_by_funded'),
    
    path('comment-on-profile/<int:profile_id>/', views.add_comment, name='add-comment'),
    path('all_comments_of_profile/<int:profile_id>/', views.get_comments_by_profile, name='get_comments_by_profile'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit-comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
]

