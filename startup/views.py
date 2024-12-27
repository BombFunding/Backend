from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import StartupProfile, StartupUser
from .serializers import StartupProfileSerializer
from rest_framework import mixins, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import IntegrityError
from rest_framework.generics import GenericAPIView
from .models import StartupProfile, StartupUser, StartupVote
from .serializers import StartupProfileSerializer, VoteSerializer
from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema

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
        Vote on a startup profile (like or nothing).
        """
        user = request.user  
        startup_profile_id = self.kwargs.get("startup_profile_id")
        vote_type = request.data.get("vote")

        if vote_type not in [1, 0]:  
            return Response(
                {"detail": "Invalid vote type."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            startup_profile = StartupProfile.objects.get(pk=startup_profile_id)
        except StartupProfile.DoesNotExist:
            return Response(
                {"detail": "Startup profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            
            existing_vote = StartupVote.objects.filter(
                user=user, startup_profile=startup_profile
            ).first()

            if vote_type == 1:  
                if existing_vote and existing_vote.vote == 1:
                    return Response(
                        {"detail": "You have already liked this profile."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                
                StartupVote.objects.update_or_create(
                    user=user, startup_profile=startup_profile, defaults={"vote": 1}
                )
                
                return Response(
                    {"detail": "Profile liked successfully."},
                    status=status.HTTP_201_CREATED,
                )

            elif vote_type == 0:  
                if existing_vote and existing_vote.vote == 1:
                    
                    existing_vote.delete()
                    return Response(
                        {"detail": "Like removed successfully."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"detail": "No like exists to remove."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        except IntegrityError:
            return Response(
                {"detail": "An error occurred while processing your vote."},
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