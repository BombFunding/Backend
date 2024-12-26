from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookmarkListView.as_view(), name='bookmark-list'),
    path('<int:project_id>/', views.BookmarkCreateView.as_view(), name='bookmark-create'),
    path('<int:project_id>/delete/', views.BookmarkDeleteView.as_view(), name='bookmark-delete'),
    path('<int:project_id>/status/', views.BookmarkStatusView.as_view(), name='bookmark-status'),
]