from authenticator.models import BaseUser
from rest_framework.permissions import BasePermission

class IsBaseUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "basic"
