from django.urls import path
from . import views

urlpatterns = [
    # ...existing code...
    path('<str:username>/', views.UserLikedCategoriesView.as_view(), name='user-liked-categories'),
    # ...existing code...
]
