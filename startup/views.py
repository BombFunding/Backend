from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import StartupProfile, Position, StartupUser
from .serializers import StartupProfileSerializer
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
from .models import StartupProfile, Position, StartupUser, StartupVote
from .serializers import StartupProfileSerializer, VoteSerializer
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from balance.utils import UserBalanceMixin
from datetime import date
from profile_statics.models import ProfileStatics


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

        if request.user.is_authenticated and request.user.username != username:
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

        excluded_fields = ["startup_profile_visit_count"]
        update_data = {key: value for key, value in request.data.items() if key not in excluded_fields}

        serializer = self.get_serializer(startup_profile, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Startup profile updated successfully.", "profile": serializer.data},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteProfile(GenericAPIView):
    permission_classes = [AllowAny]

    def get_permissions(self):
        """
        Different permission classes for functions
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
        user = request.user  # This is an instance of BaseUser
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
            # Create or update the vote
            startup_vote, created = StartupVote.objects.update_or_create(
                user=user, startup_profile=startup_profile, defaults={"vote": vote_type}
            )

            # Ensure ProfileStatics exists for the startup profile's user
            profile_statics, _ = ProfileStatics.objects.get_or_create(
                user=startup_profile.startup_user.username
            )

            # Update likes based on vote type
            if vote_type == 1:
                profile_statics.add_like(liked_by_user=user.username)
            elif vote_type == -1:
                profile_statics.remove_like(liked_by_user=user.username)

            # Return appropriate response
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