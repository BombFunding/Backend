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


@api_view(["GET"])
@permission_classes([AllowAny])
def sort_positions_by_funded(request):
    order = request.query_params.get("order", "asc")
    if order == "asc":
        positions = StartupPosition.objects.all().order_by("funded")
    else:
        positions = StartupPosition.objects.all().order_by("-funded")

    result = [
        {
            "name": pos.name,
            "bio": pos.bio,
            "total": pos.total,
            "funded": pos.funded,
            "is_done": pos.is_done,
            "start_time": pos.start_time,
            "end_time": pos.end_time,
        }
        for pos in positions
    ]

    return JsonResponse({"positions": result}, safe=False)


@api_view(["GET"])
@permission_classes([AllowAny])
def sort_positions_by_date(request):
    order = request.query_params.get("order", "asc")
    if order == "asc":
        positions = StartupPosition.objects.all().order_by("start_time")
    else:
        positions = StartupPosition.objects.all().order_by("-start_time")

    result = [
        {
            "name": pos.name,
            "bio": pos.bio,
            "total": pos.total,
            "funded": pos.funded,
            "is_done": pos.is_done,
            "start_time": pos.start_time,
            "end_time": pos.end_time,
        }
        for pos in positions
    ]

    return JsonResponse({"positions": result}, safe=False)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_positions(request):
    try:
        positions = StartupPosition.objects.all()
        result = [
            {
                "id": pos.id,
                "name": pos.name,
                "bio": pos.bio,
                "total": pos.total,
                "funded": pos.funded,
                "is_done": pos.is_done,
                "start_time": pos.start_time,
                "end_time": pos.end_time,
                "startup_profile": {
                    "startup_profile_id": pos.startup_profile.id,
                    "name": pos.startup_profile.name,
                },
            }
            for pos in positions
        ]

        return JsonResponse({"positions": result}, safe=False)

    except Exception as e:
        return JsonResponse({"detail": f"Error: {str(e)}"}, status=500)


@api_view(["GET"])
@permission_classes([AllowAny])
def search_positions_by_date_range(request):
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")

    if not start_date or not end_date:
        return JsonResponse(
            {"detail": "Both 'start_date' and 'end_date' are required."}, status=400
        )

    parsed_start_date = parse_datetime(start_date + "T00:00:00Z")
    parsed_end_date = parse_datetime(end_date + "T23:59:59Z")

    if not parsed_start_date or not parsed_end_date:
        return JsonResponse(
            {"detail": "Invalid date format. Use YYYY-MM-DD."}, status=400
        )

    positions = StartupPosition.objects.filter(
        end_time__gte=parsed_start_date, end_time__lte=parsed_end_date
    )

    result = [
        {
            "name": pos.name,
            "bio": pos.bio,
            "total": pos.total,
            "funded": pos.funded,
            "is_done": pos.is_done,
            "start_time": pos.start_time,
            "end_time": pos.end_time,
        }
        for pos in positions
    ]

    return JsonResponse({"positions": result}, safe=False)


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



