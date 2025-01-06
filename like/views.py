from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Like
from .serializers import LikeSerializer, LikeCountSerializer, HasLikedSerializer
from project.models import Project
from drf_yasg.utils import swagger_auto_schema, no_body
from profile_statics.models import ProjectStatistics

class LikeCreateView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=no_body, responses={201: LikeSerializer()})
    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs.get('project_id'))
        
        if Like.objects.filter(user=request.user, project=project).exists():
            return Response(
                {'error': 'You have already liked this project'},
                status=status.HTTP_400_BAD_REQUEST
            )

        project_statistics = ProjectStatistics.objects.get_or_create(project=project)[0]
        project_statistics.add_like(request.user.username)

        like = Like.objects.create(user=request.user, project=project)
        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=no_body, responses={204: "No Content"})
    def delete(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs.get('project_id'))

        project_statistics = ProjectStatistics.objects.get_or_create(project=project)[0]
        project_statistics.remove_like(request.user.username)

        try:
            like = Like.objects.get(user=request.user, project=project)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response(
                {'error': 'You have not liked this project'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProjectLikeCountView(generics.RetrieveAPIView):
    permission_classes = []
    serializer_class = LikeCountSerializer

    @swagger_auto_schema(responses={200: LikeCountSerializer()})
    def retrieve(self, request, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return Response({'likes': 0})
            
        project = get_object_or_404(Project, id=self.kwargs.get('project_id'))
        like_count = Like.objects.filter(project=project).count()
        serializer = self.get_serializer({'likes': like_count})
        return Response(serializer.data)

class StartupLikeCountView(generics.RetrieveAPIView):
    permission_classes = []
    serializer_class = LikeCountSerializer

    @swagger_auto_schema(responses={200: LikeCountSerializer()})
    def retrieve(self, request, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return Response({'likes': 0})
            
        startup_username = self.kwargs.get('username')
        
        total_likes = Like.objects.filter(
            project__user__username=startup_username
        ).count()

        serializer = self.get_serializer({'likes': total_likes})
        return Response(serializer.data)

class CheckLikeView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HasLikedSerializer

    @swagger_auto_schema(responses={200: HasLikedSerializer()})
    def retrieve(self, request, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            return Response({'has_liked': False})
            
        project = get_object_or_404(Project, id=self.kwargs.get('project_id'))
        has_liked = Like.objects.filter(
            user=request.user,
            project=project
        ).exists()
        serializer = self.get_serializer({'has_liked': has_liked})
        return Response(serializer.data)


