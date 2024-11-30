from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from authenticator.serializers import BaseProfileSerializer
from .models import (
    StartupPosition,
    BaseProfile,
    StartupUser,
)
from .serializers import (
    StartupPositionSerializer,
)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_update_position(request):
    user = request.user

    if user.user_type != "startup":
        return Response(
            {
                "detail": "Only users with 'startup' type can create or update a startup position."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        startup_user = StartupUser.objects.get(username=user)
    except StartupUser.DoesNotExist:
        return Response(
            {"detail": "No related startup found."}, status=status.HTTP_404_NOT_FOUND
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
        message = "Position updated successfully."
    except StartupPosition.DoesNotExist:
        serializer = StartupPositionSerializer(data=request.data)
        message = "Position created successfully."

    if serializer.is_valid():
        serializer.save(startup_profile=startup_profile)
        return Response(
            {"detail": message, "position": serializer.data}, status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



