from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import StartupProfile, StartupPosition, StartupUser
from .serializers import StartupProfileSerializer, StartupPositionSerializer

class StartupProfileViews:
    @staticmethod
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

        if request.user.username != username:
            startup_profile.startup_profile_visit_count += 1
            startup_profile.save()

        serializer = StartupProfileSerializer(startup_profile)
        return JsonResponse(
            {"profile": serializer.data}, status=status.HTTP_200_OK
        )

    @staticmethod
    @api_view(["PATCH"])
    @permission_classes([IsAuthenticated])
    def update_startup_profile(request):
        user = request.user

        if user.user_type != "startup":
            return Response(
                {"detail": "Only users with 'startup' type can update a startup profile."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            startup_user = StartupUser.objects.get(username=user)
        except StartupUser.DoesNotExist:
            return Response(
                {"detail": "Startup user not found."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            startup_profile = StartupProfile.objects.get(startup_user=startup_user)
        except StartupProfile.DoesNotExist:
            return Response(
                {"detail": "Startup profile not found."}, status=status.HTTP_404_NOT_FOUND
            )

        excluded_fields = ["startup_profile_visit_count", "startupposition_set", "startup_rank"]
        update_data = {
            key: value
            for key, value in request.data.items()
            if key not in excluded_fields
        }

        serializer = StartupProfileSerializer(
            startup_profile, data=update_data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Startup profile updated successfully.", "profile": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StartupPositionViews:
    @staticmethod
    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def create_startup_position(request):
        user = request.user

        if user.user_type != "startup":
            return Response(
                {"detail": "Only users with 'startup' type can create positions."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            startup_profile = StartupProfile.objects.get(startup_user=user.startupuser)
        except StartupProfile.DoesNotExist:
            return Response(
                {"detail": "Startup profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = StartupPositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(startup_profile=startup_profile)
            return Response(
                {"detail": "Position created successfully.", "position": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_view(["PATCH"])
    @permission_classes([IsAuthenticated])
    def update_startup_position(request, position_id):
        user = request.user

        if user.user_type != "startup":
            return Response(
                {"detail": "Only users with 'startup' type can update positions."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            startup_profile = StartupProfile.objects.get(startup_user=user.startupuser)
        except StartupProfile.DoesNotExist:
            return Response(
                {"detail": "Startup profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            position = StartupPosition.objects.get(id=position_id, startup_profile=startup_profile)
        except StartupPosition.DoesNotExist:
            return Response(
                {"detail": "Position not found or not owned by this startup."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = StartupPositionSerializer(position, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Position updated successfully.", "position": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
