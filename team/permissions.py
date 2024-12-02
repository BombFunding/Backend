from rest_framework import permissions
from startup.models import StartupProfile
from authenticator.models import StartupUser

class IsStartupUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return StartupUser.objects.filter(username=request.user).exists()
    
        
class IsStartupOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        startup_profile_id = view.kwargs["startup_profile_id"]
        user = request.user

        try:
            print("FAILED TO GET USER")
            startup_user = StartupUser.objects.get(username=user)
        except StartupUser.DoesNotExist:
            return False

        try:
            print("FAILED TO GET STARTUP")
            startup = StartupProfile.objects.get(id=startup_profile_id, startup_user=startup_user)
        except StartupProfile.DoesNotExist:
            return False

        return True