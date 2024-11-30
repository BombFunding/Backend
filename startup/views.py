from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext as _

from authenticator.serializers import BaseProfileSerializer
from .models import (
    StartupProfile,
    StartupPosition,
    BaseProfile,
    StartupUser,
)
from .serializers import (
    StartupPositionSerializer,
    StartupProfileSerializer
)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_update_position(request):
    user = request.user

    if user.user_type != "startup":
        return Response(
            {
                str(_("error")): _("Only users with type 'startup' can create or update startup positions.")
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        startup_user = StartupUser.objects.get(username=user)
    except StartupUser.DoesNotExist:
        return Response(
            {str(_("error")): _("Related startup not found.")}, status=status.HTTP_404_NOT_FOUND
        )

    try:
        startup_profile = BaseProfile.objects.get(startup_user=startup_user)
    except BaseProfile.DoesNotExist:
        startup_profile = BaseProfile.objects.create(
            startup_user=startup_user, name="Default Name", bio="Default bio"
        )

    position_name = request.data.get("name")
    try:
        position = StartupPosition.objects.get(
            startup_profile=startup_profile, name=position_name
        )

        serializer = StartupPositionSerializer(
            position, data=request.data, partial=True
        )
        message = "Position successfully updated."
    except StartupPosition.DoesNotExist:
        serializer = StartupPositionSerializer(data=request.data)
        message = "Position successfully created."

    if serializer.is_valid():
        serializer.save(startup_profile=startup_profile)
        return Response(
            {str(_("message")): _("Position successfully updated."), "position": serializer.data}, status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_startup_profile(request, username):
    try:
        
        startup_user = StartupUser.objects.get(username__username=username)
    except StartupUser.DoesNotExist:
        return JsonResponse(
            {"detail": "Startup user not found."}, status=status.HTTP_404_NOT_FOUND
        )

    
    startup_profile = StartupProfile.objects.filter(startup_user=startup_user).first()

    if not startup_profile:
        return JsonResponse(
            {"detail": "Startup profile not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = StartupProfileSerializer(startup_profile)
    return JsonResponse(
        {"profile": serializer.data}, status=status.HTTP_200_OK
    )
