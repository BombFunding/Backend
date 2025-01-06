from django.urls import path
from .views import LikeCreateView, ProjectLikeCountView, StartupLikeCountView, CheckLikeView

urlpatterns = [
    path('<int:project_id>/', LikeCreateView.as_view(), name='like-project'),
    path('<int:project_id>/count/', ProjectLikeCountView.as_view(), name='project-like-count'),
    path('startup/<str:username>/', StartupLikeCountView.as_view(), name='startup-like-count'),
    path('check/<int:project_id>/', CheckLikeView.as_view(), name='check-like'),
]
