from rest_framework import permissions
from .models import BookmarkUser

class IsBookmarkOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        bookmark_id = view.kwargs["pk"]
        user = request.user

        try:
            bookmark = BookmarkUser.objects.get(id=bookmark_id, owner=user)
        except BookmarkUser.DoesNotExist:
            return False

        return True