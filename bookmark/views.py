from rest_framework import generics, permissions

from .serializers import BookmarkSerializer
from .permissions import IsBookmarkOwner
from .models import BookmarkUser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class BookmarkView(generics.ListCreateAPIView):
    queryset = BookmarkUser.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Create a bookmark",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'target': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user to bookmark'),
            },
        ),
        responses={
            201: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the bookmark'),
                    'target_username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the bookmarked user'),
                },
            ),
            400: 'Bad Request',
            401: 'Unauthorized',
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="List all bookmarks",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the bookmark'),
                        'target_username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the bookmarked user'),
                    },
                ),
            ),
            401: 'Unauthorized',
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class DestroyBookmarkView(generics.DestroyAPIView):
    queryset = BookmarkUser.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookmarkOwner]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return BookmarkUser.objects.none()
        return self.queryset.filter(owner=self.request.user)