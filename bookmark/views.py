from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from project.models import Project
from .models import Bookmark
from .serializers import BookmarkStatusSerializer, BookmarkedProjectSerializer
from drf_yasg.utils import swagger_auto_schema

class BookmarkCreateView(APIView):
    @swagger_auto_schema(
        operation_description="Bookmark a project",
        responses={201: "Created", 400: "Already bookmarked"}
    )
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if Bookmark.objects.filter(owner=request.user, target=project).exists():
            return Response({"error": "Already bookmarked"}, status=status.HTTP_400_BAD_REQUEST)
        
        Bookmark.objects.create(owner=request.user, target=project)
        return Response(status=status.HTTP_201_CREATED)

class BookmarkDeleteView(APIView):
    @swagger_auto_schema(
        operation_description="Delete a bookmark",
        responses={204: "No Content", 400: "Not bookmarked"}
    )
    def delete(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        bookmark = Bookmark.objects.filter(owner=request.user, target=project).first()
        
        if not bookmark:
            return Response({"error": "Not bookmarked"}, status=status.HTTP_400_BAD_REQUEST)
        
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookmarkStatusView(APIView):
    @swagger_auto_schema(
        operation_description="Check if a project is bookmarked",
        responses={200: BookmarkStatusSerializer}
    )
    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        has_bookmarked = Bookmark.objects.filter(owner=request.user, target=project).exists()
        serializer = BookmarkStatusSerializer({"has_bookmarked": has_bookmarked})
        return Response(serializer.data)

class BookmarkListView(APIView):
    @swagger_auto_schema(
        operation_description="Get all bookmarked projects of a user",
        responses={200: BookmarkedProjectSerializer(many=True)}
    )
    def get(self, request):
        bookmarks = Bookmark.objects.filter(owner=request.user)
        serializer = BookmarkedProjectSerializer(bookmarks, many=True)
        return Response(serializer.data)
