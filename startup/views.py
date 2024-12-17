from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import StartupProfile, StartupPosition, StartupUser
from .serializers import StartupProfileSerializer, StartupPositionSerializer
from rest_framework import mixins, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import StartupProfile, StartupPosition, StartupUser, StartupVote
from .serializers import StartupProfileSerializer, StartupPositionSerializer, VoteSerializer
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from balance.utils import UserBalanceMixin
from datetime import date
from profile_statics.models import ProfileStatics

POSITION_CREATION_COST = 100000

class StartupProfileRetrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = StartupProfile.objects.all()
    serializer_class = StartupProfileSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Get the profile of a startup user",
        responses={
            200: openapi.Response(
                description="Profile retrieved successfully.",
                examples={
                    "application/json": {
                        "profile": {
                            "id": 2,
                            "startup_user": 3,
                            "startup_categories": "Technology",
                            "startup_starting_date": None,
                            "startup_profile_visit_count": 2,
                            "positions": [
                                {
                                    "id": 1,
                                    "name": "string",
                                    "description": "string",
                                    "total": 9223372854776000,
                                    "funded": 922337203776000,
                                    "is_done": True,
                                    "start_time": "2024-12-06T23:50:23.585000Z",
                                    "end_time": "2024-12-06T23:50:23.585000Z"
                                }
                            ]
                        }
                    }
                },
            ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "detail": "Profile not found."
                    }
                },
            ),
        },
    )
    def get(self, request, username):
        try:
            startup_user = StartupUser.objects.get(username__username=username)
        except StartupUser.DoesNotExist:
            return Response({"detail": "Startup user not found."}, status=status.HTTP_404_NOT_FOUND)

        startup_profile = StartupProfile.objects.filter(startup_user=startup_user).first()

        if not startup_profile:
            return Response({"detail": "Startup profile not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.username != username:
            startup_profile.startup_profile_visit_count += 1
            startup_profile.save()
            profile_statics = ProfileStatics.objects.get(user=startup_user.username)
            profile_statics.increment_view() 

        serializer = self.get_serializer(startup_profile)
        return Response({"profile": serializer.data}, status=status.HTTP_200_OK)

class StartupProfileUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = StartupProfile.objects.all()
    serializer_class = StartupProfileSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user

        if user.user_type != "startup":
            return Response({"detail": "Only users with 'startup' type can update a startup profile."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            startup_user = StartupUser.objects.get(username=user)
        except StartupUser.DoesNotExist:
            return Response({"detail": "Startup user not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            startup_profile = StartupProfile.objects.get(startup_user=startup_user)
        except StartupProfile.DoesNotExist:
            return Response({"detail": "Startup profile not found."}, status=status.HTTP_404_NOT_FOUND)

        excluded_fields = ["startup_profile_visit_count", "startupposition_set"]
        update_data = {key: value for key, value in request.data.items() if key not in excluded_fields}

        serializer = self.get_serializer(startup_profile, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Startup profile updated successfully.", "profile": serializer.data},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import StartupPosition
from .serializers import StartupPositionSerializer

class StartupPositionListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = StartupPosition.objects.all()
    serializer_class = StartupPositionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all positions of the authenticated startup user.",
        responses={
            200: openapi.Response(
                description="List of startup positions.",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "startup_profile": 2,
                            "name": "Tech Innovators Fund",
                            "description": "Funding for a groundbreaking tech startup.",
                            "total": 100000,
                            "funded": 50000,
                            "is_done": False,
                            "start_time": "2024-12-01T09:00:00Z",
                            "end_time": "2024-12-31T18:00:00Z"
                        },
                        {
                            "id": 2,
                            "startup_profile": 2,
                            "name": "Green Energy Ventures",
                            "description": "Fundraising for sustainable energy solutions.",
                            "total": 200000,
                            "funded": 180000,
                            "is_done": False,
                            "start_time": "2024-11-01T09:00:00Z",
                            "end_time": "2024-12-15T18:00:00Z"
                        }
                    ]
                }
            ),
            403: openapi.Response(description="Forbidden - User is not a startup."),
        }
    )
    def get(self, request):
        user = request.user

        if user.user_type != "startup":
            return Response({"detail": "Only users with 'startup' type can view positions."},
                            status=status.HTTP_403_FORBIDDEN)

        positions = StartupPosition.objects.filter(startup_profile__startup_user=user.startupuser)
        serializer = self.get_serializer(positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StartupPositionCreateView(mixins.CreateModelMixin, generics.GenericAPIView, UserBalanceMixin):
    queryset = StartupPosition.objects.all()
    serializer_class = StartupPositionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.user_type != "startup":
            return Response({"detail": "Only users with 'startup' type can create positions."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            startup_profile = StartupProfile.objects.get(startup_user=user.startupuser)
        except StartupProfile.DoesNotExist:
            return Response({"detail": "Startup profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(startup_profile=startup_profile)
            self.reduce_balance(user, POSITION_CREATION_COST)
            return Response({"detail": "Position created successfully.", "position": serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StartupPositionUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = StartupPosition.objects.all()
    serializer_class = StartupPositionSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, position_id):
        user = request.user

        if user.user_type != "startup":
            return Response({"detail": "Only users with 'startup' type can update positions."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            startup_profile = StartupProfile.objects.get(startup_user=user.startupuser)
        except StartupProfile.DoesNotExist:
            return Response({"detail": "Startup profile not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            position = StartupPosition.objects.get(id=position_id, startup_profile=startup_profile)
        except StartupPosition.DoesNotExist:
            return Response({"detail": "Position not found or not owned by this startup."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(position, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Position updated successfully.", "position": serializer.data},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StartupPositionDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = StartupPosition.objects.all()
    serializer_class = StartupPositionSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, position_id):
        user = request.user

        if user.user_type != "startup":
            return Response({"detail": "Only users with 'startup' type can delete positions."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            startup_profile = StartupProfile.objects.get(startup_user=user.startupuser)
        except StartupProfile.DoesNotExist:
            return Response({"detail": "Startup profile not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            position = StartupPosition.objects.get(id=position_id, startup_profile=startup_profile)
        except StartupPosition.DoesNotExist:
            return Response({"detail": "Position not found or not owned by this startup."}, status=status.HTTP_404_NOT_FOUND)

        position.delete()
        return Response({"detail": "Position deleted successfully."}, status=status.HTTP_200_OK)


class VoteProfile(GenericAPIView):
    permission_classes = [AllowAny]

    def get_permissions(self):
        """
        diffrent permission classes for functions
        """
        if self.request.method in ["POST", "DELETE"]:
            return [IsAuthenticated()]
        return super().get_permissions()

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