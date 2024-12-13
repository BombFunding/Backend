from django.urls import path

from . import views

urlpatterns = [
    path("", views.BookmarkView.as_view()),
    path("<int:pk>/", views.DestroyBookmarkView.as_view()),
]