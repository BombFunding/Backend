from rest_framework import generics, permissions

from .models import BookmarkUser
from .serializers import BookmarkSerializer
from .permissions import IsBookmarkOwner


class BookmarkView(generics.ListCreateAPIView):
    queryset = BookmarkUser.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DestroyBookmarkView(generics.DestroyAPIView):
    queryset = BookmarkUser.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookmarkOwner]

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)