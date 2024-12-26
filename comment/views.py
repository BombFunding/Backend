from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Comment
from project.models import Project
from .serializers import CommentInputSerializer, CommentOutputSerializer

class CommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentInputSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a comment (the user must be authenticated)",
        request_body=CommentInputSerializer,
        responses={200: CommentInputSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, project=Project.objects.get(id=self.kwargs['project_id']))

class CommentListView(generics.ListAPIView):
    serializer_class = CommentOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all comments for a project",
        responses={200: CommentOutputSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Comment.objects.filter(project_id=project_id)

class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete a comment (only the comment author can delete it)",
        responses={
            204: "Comment deleted successfully",
            403: "Forbidden - Not the comment author",
            404: "Comment not found"
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            comment = self.get_object()
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        return Comment.objects.get(
            id=self.kwargs['comment_id'],
            project_id=self.kwargs['project_id']
        )

class CommentUpdateView(generics.UpdateAPIView):
    serializer_class = CommentInputSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    @swagger_auto_schema(
        operation_description="Edit a comment (only the comment author can edit it)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['text']
        ),
        responses={
            200: CommentOutputSerializer,
            403: "Forbidden - Not the comment author",
            404: "Comment not found"
        }
    )
    def patch(self, request, *args, **kwargs):
        try:
            comment = self.get_object()
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        if comment.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        return super().patch(request, *args, **kwargs)

    def get_object(self):
        return Comment.objects.get(
            id=self.kwargs['comment_id'],
            project_id=self.kwargs['project_id']
        )

