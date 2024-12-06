from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext as _
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema

from .models import (
    StartupProfile,
    StartupPosition,
    BaseProfile,
    StartupUser,
    StartupVote,
)
from .serializers import (
    StartupPositionSerializer,
    StartupProfileSerializer,
    VoteSerializer,
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_update_position(request):
    user = request.user

    if user.user_type != "startup":
        return Response(
            {
                str(_("error")): _(
                    "Only users with type 'startup' can create or update startup positions."
                )
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        startup_user = StartupUser.objects.get(username=user)
    except StartupUser.DoesNotExist:
        return Response(
            {str(_("error")): _("Related startup not found.")},
            status=status.HTTP_404_NOT_FOUND,
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
            {str(_("message")): _(message), "position": serializer.data}, status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_startup_profile(request, username):
    try:

        startup_user = StartupUser.objects.get(username__username=username)
    except StartupUser.DoesNotExist:
        return JsonResponse(
            {_("detail"): _("Startup user not found.")}, status=status.HTTP_404_NOT_FOUND
        )

    startup_profile = StartupProfile.objects.filter(startup_user=startup_user).first()

    if not startup_profile:
        return JsonResponse(
            {_("detail"): _("Startup profile not found.")}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = StartupProfileSerializer(startup_profile)
    return JsonResponse({"profile": serializer.data}, status=status.HTTP_200_OK)


class VoteProfile(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=VoteSerializer,
        responses={
            201: "Vote added successfully.",
            200: "Vote updated successfully.",
            400: "Invalid vote type.",
            404: "Startup profile not found.",
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Vote on a startup profile.
        """
        user = request.user
        startup_profile_id = self.kwargs.get("startup_profile_id")
        vote_type = request.data.get("vote")

        if vote_type not in [1, -1]:
            return Response(
                {"detail": "Invalid vote type."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            startup_profile = StartupProfile.objects.get(pk=startup_profile_id)
        except StartupProfile.DoesNotExist:
            return Response(
                {"detail": "Startup profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            startup_vote, created = StartupVote.objects.update_or_create(
                user=user, startup_profile=startup_profile, defaults={"vote": vote_type}
            )
            if created:
                return Response(
                    {"detail": "Vote added successfully."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"detail": "Vote updated successfully."}, status=status.HTTP_200_OK
                )
        except IntegrityError:
            return Response(
                {"detail": "You have already voted on this profile."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        responses={
            204: "Vote removed successfully.",
            400: "You have not voted on this profile.",
            404: "Startup profile not found.",
        },
    )
    def delete(self, request, *args, **kwargs):
        """
        Remove a vote from a startup profile.
        """
        user = request.user
        startup_profile_id = self.kwargs.get("startup_profile_id")

        try:
            startup_profile = StartupProfile.objects.get(pk=startup_profile_id)
        except StartupProfile.DoesNotExist:
            return Response(
                {"detail": "Startup profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            startup_vote = StartupVote.objects.get(
                user=user, startup_profile=startup_profile
            )
            startup_vote.delete()
            return Response(
                {"detail": "Vote removed successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except StartupVote.DoesNotExist:
            return Response(
                {"detail": "You have not voted on this profile."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        responses={
            200: "Vote count retrieved successfully.",
            404: "Startup profile not found.",
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Get the vote count of a startup profile.
        """
        startup_profile_id = self.kwargs.get("startup_profile_id")

        try:
            startup_profile = StartupProfile.objects.get(pk=startup_profile_id)
        except StartupProfile.DoesNotExist:
            return Response(
                {"detail": "Startup profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        vote_count = startup_profile.score
        return Response(
            {"vote_count": vote_count},
            status=status.HTTP_200_OK,
        )
