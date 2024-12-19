from rest_framework import permissions
from startup.models import StartupProfile
from authenticator.models import StartupUser
from authenticator.utils import get_instance


class IsStartupOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        startup_user = get_instance(StartupUser, username=user)
        if not startup_user:
            return False
        startup_profile_id = view.kwargs.get("startup_profile_id")
        startup_profile = get_instance(StartupProfile, id=startup_profile_id, startup_user=startup_user)
        if not startup_profile:
            return False
        return True
