from django.urls import path
from .views import ProjectListCreateView, ProjectRetrieveUpdateDestroyView, ProjectImageView, ProjectDetailView

urlpatterns = [
    path('', ProjectListCreateView.as_view(), name='project-list-create'),
    path('<int:pk>/', ProjectRetrieveUpdateDestroyView.as_view(), name='project-detail'),
    path('image/', ProjectImageView.as_view(), name='project-image'),
    path('detail/<int:pk>/', ProjectDetailView.as_view(), name='project-detail-view'),
]