from django.urls import path
from .views import CommentView, CommentListView, CommentDeleteView, CommentUpdateView

urlpatterns = [
    path('<int:project_id>/', CommentView.as_view(), name='comment-create'),
    path('list/<int:project_id>/', CommentListView.as_view(), name='comment-list'),
    path('<int:project_id>/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('<int:project_id>/<int:comment_id>/edit/', CommentUpdateView.as_view(), name='comment-edit'),
]
