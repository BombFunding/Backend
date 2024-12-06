from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
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

<<<<<<<<< Temporary merge branch 1
from django.utils.translation import gettext as _

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
=========
from .models import StartupProfile, StartupPosition, StartupUser
from .serializers import StartupProfileSerializer, StartupPositionSerializer

class StartupProfileRetrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = StartupProfile.objects.all()
    serializer_class = StartupProfileSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Get the profile of a startup user",
        responses={200: StartupProfileSerializer, 404: 'Not Found'},
    )
    def get(self, request, username):
        try:
            startup_user = StartupUser.objects.get(username__username=username)
        except StartupUser.DoesNotExist:
            return JsonResponse(
                {"detail": "Startup user not found."}, status=status.HTTP_404_NOT_FOUND
            )
>>>>>>>>> Temporary merge branch 2

        startup_profile = StartupProfile.objects.filter(startup_user=startup_user).first()

        if not startup_profile:
            return Response({"detail": "Startup profile not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user.username != username:
            startup_profile.startup_profile_visit_count += 1
            startup_profile.save()

        serializer = self.get_serializer(startup_profile)
        return Response({"profile": serializer.data}, status=status.HTTP_200_OK)

class StartupProfileUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = StartupProfile.objects.all()
    serializer_class = StartupProfileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update the startup profile",
        request_body=StartupProfileSerializer,
        responses={200: StartupProfileSerializer, 400: 'Bad Request', 403: 'Forbidden'},
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token for authentication", type=openapi.TYPE_STRING)
        ]
    )
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

        excluded_fields = ["startup_profile_visit_count", "startupposition_set", "startup_rank"]
        update_data = {key: value for key, value in request.data.items() if key not in excluded_fields}

        serializer = StartupProfileSerializer(
            startup_profile, data=update_data, partial=True
>>>>>>>>> Temporary merge branch 2
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Startup profile updated successfully.", "profile": serializer.data},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StartupPositionCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = StartupPosition.objects.all()
    serializer_class = StartupPositionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new startup position",
        request_body=StartupPositionSerializer,
        responses={201: StartupPositionSerializer, 400: 'Bad Request', 403: 'Forbidden'},
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token for authentication", type=openapi.TYPE_STRING)
        ]
    )
    def post(self, request):
        user = request.user

        if user.user_type != "startup":
            return Response({"detail": "Only users with 'startup' type can create positions."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            startup_profile = StartupProfile.objects.get(startup_user=user.startupuser)
        except StartupProfile.DoesNotExist:
            return Response(
                {"detail": "Startup profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

<<<<<<<<< Temporary merge branch 1
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
=========
        serializer = StartupPositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(startup_profile=startup_profile)
            return Response({"detail": "Position created successfully.", "position": serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
>>>>>>>>> Temporary merge branch 2

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

<<<<<<<<< Temporary merge branch 1
@api_view(["GET"])
@permission_classes([AllowAny])
def get_startup_profile(request, username):
    try:
        
        startup_user = StartupUser.objects.get(username__username=username)
    except StartupUser.DoesNotExist:
        return JsonResponse(
            {_("detail"): _("Startup user not found.")}, status=status.HTTP_404_NOT_FOUND
        )
=========
        try:
            startup_profile = StartupProfile.objects.get(startup_user=user.startupuser)
        except StartupProfile.DoesNotExist:
            return Response(
                {"detail": "Startup profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
>>>>>>>>> Temporary merge branch 2

        try:
            position = StartupPosition.objects.get(id=position_id, startup_profile=startup_profile)
        except StartupPosition.DoesNotExist:
            return Response(
                {"detail": "Position not found or not owned by this startup."},
                status=status.HTTP_404_NOT_FOUND,
            )

<<<<<<<<< Temporary merge branch 1
    if not startup_profile:
        return JsonResponse(
            {_("detail"): _("Startup profile not found.")}, status=status.HTTP_404_NOT_FOUND
        )
=========
        serializer = StartupPositionSerializer(position, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Position updated successfully.", "position": serializer.data},
                status=status.HTTP_200_OK,
            )
>>>>>>>>> Temporary merge branch 2

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import StartupProfile, StartupPosition, StartupUser
from .serializers import StartupProfileSerializer, StartupPositionSerializer
from rest_framework import mixins, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class StartupProfileRetrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = StartupProfile.objects.all()
    serializer_class = StartupProfileSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Get the profile of a startup user",
        responses={200: StartupProfileSerializer, 404: 'Not Found'},
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

        serializer = self.get_serializer(startup_profile)
        return Response({"profile": serializer.data}, status=status.HTTP_200_OK)

class StartupProfileUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = StartupProfile.objects.all()
    serializer_class = StartupProfileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update the startup profile",
        request_body=StartupProfileSerializer,
        responses={200: StartupProfileSerializer, 400: 'Bad Request', 403: 'Forbidden'},
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token for authentication", type=openapi.TYPE_STRING)
        ]
    )
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

        excluded_fields = ["startup_profile_visit_count", "startupposition_set", "startup_rank"]
        update_data = {key: value for key, value in request.data.items() if key not in excluded_fields}

        serializer = self.get_serializer(startup_profile, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Startup profile updated successfully.", "profile": serializer.data},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StartupPositionCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = StartupPosition.objects.all()
    serializer_class = StartupPositionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new startup position",
        request_body=StartupPositionSerializer,
        responses={201: StartupPositionSerializer, 400: 'Bad Request', 403: 'Forbidden'},
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token for authentication", type=openapi.TYPE_STRING)
        ]
    )
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
            return Response({"detail": "Position created successfully.", "position": serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StartupPositionUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = StartupPosition.objects.all()
    serializer_class = StartupPositionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update an existing startup position",
        request_body=StartupPositionSerializer,
        responses={200: StartupPositionSerializer, 400: 'Bad Request', 403: 'Forbidden'},
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token for authentication", type=openapi.TYPE_STRING)
        ]
    )
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

    @swagger_auto_schema(
        operation_description="Delete an existing startup position",
        responses={200: 'Position deleted successfully.', 403: 'Forbidden', 404: 'Not Found'},
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer token for authentication", type=openapi.TYPE_STRING)
        ]
    )
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
