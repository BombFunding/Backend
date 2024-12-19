from django.shortcuts import render
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Position
from .serializers import PositionSerializer
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Position
from .serializers import PositionSerializer
from authenticator.models import BaseUser
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from balance.utils import UserBalanceMixin

POSITION_CREATION_COST_PER_DAY = 100000


class PositionListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve all positions of the authenticated user (startup or investor).",
        responses={
            200: openapi.Response(
                description="List of positions.",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "position_user": 2,
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
                            "position_user": 2,
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
            403: openapi.Response(description="Forbidden - User is not a startup or investor."),
        }
    )
    def get(self, request, username):
        try:
            user = BaseUser.objects.get(username=username)
        except BaseUser.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        positions = Position.objects.filter(position_user=user)
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PositionCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.user_type not in ["startup", "investor"]:
            return Response(
                {"detail": "Only users with 'startup' or 'investor' type can create positions."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            
            start_time = serializer.validated_data.get("start_time")
            end_time = serializer.validated_data.get("end_time")

            
            delta = (end_time - start_time).days
            if delta < 1:  
                return Response(
                    {"detail": "The duration must be at least 1 day."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            
            mixin = UserBalanceMixin()
            mixin.reduce_balance(user, POSITION_CREATION_COST_PER_DAY * delta)

            
            serializer.save(position_user=user)
            return Response(
                {"detail": "Position created successfully.", "position": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PositionUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, position_id):
        user = request.user

        if user.user_type not in ["startup", "investor"]:
            return Response(
                {"detail": "Only users with 'startup' or 'investor' type can update positions."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            position = Position.objects.get(id=position_id, position_user=user)
        except Position.DoesNotExist:
            return Response(
                {"detail": "Position not found or not owned by this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(position, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Position updated successfully.", "position": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PositionDeleteView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, position_id):
        user = request.user

        if user.user_type not in ["startup", "investor"]:
            return Response(
                {"detail": "Only users with 'startup' or 'investor' type can delete positions."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            position = Position.objects.get(id=position_id, position_user=user)
        except Position.DoesNotExist:
            return Response(
                {"detail": "Position not found or not owned by this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        position.delete()
        return Response({"detail": "Position deleted successfully."}, status=status.HTTP_200_OK)