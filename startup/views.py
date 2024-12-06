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
