from django.utils import timezone
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import Position
from .serializers import PositionSerializer
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, generics
from drf_yasg import openapi
from datetime import timedelta  
from rest_framework.exceptions import ValidationError 
from balance.utils import UserBalanceMixin
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from .serializers import PositionDetailSerializer, PositionCreateSerializer, PositionUpdateSerializer
from project.models import Project
from django.views.generic.edit import CreateView
from bookmark.models import Bookmark
from notifications.models import send_notification


POSITION_CREATION_BASE_COST = 100000
POSITION_CREATION_COST_PER_DAY = 10000
POSITION_RENEWAL_COST_3_DAY = 25000
POSITION_RENEWAL_COST_7_DAY = 50000
POSITION_RENEWAL_COST_10_DAY = 80000


class PositionCreateView(generics.CreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionCreateSerializer

    @swagger_auto_schema(
        operation_description="Create a new position.",
    )
    def post(self, request, *args, **kwargs):
        project_id = kwargs.get('project_id')

        # Check for existing open positions
        if Position.objects.filter(project_id=project_id, end_time__gt=timezone.now()).exists():
            return Response(
                {"detail": "You already have an open position for this project."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate the cost
        end_time_str = request.data.get('end_time')
        start_time = request.data.get('start_time', timezone.now())

        end_time = timezone.datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S')
        if timezone.is_naive(end_time):
            end_time = timezone.make_aware(end_time)

        days = (end_time - start_time).days
        cost = POSITION_CREATION_COST_PER_DAY * days

        # Apply the cost to the project owner
        project = Project.objects.get(id=project_id)
        owner = project.user
        mixin = UserBalanceMixin()
        mixin.reduce_balance(owner, cost)

        # Send notifications to users who have bookmarked the project
        bookmarks = Bookmark.objects.filter(target=project)
        for bookmark in bookmarks:
            send_notification(bookmark.owner, f"یک موقعیت جدید برای پروژه {project.name} ایجاد شده است.", "position_created_bookmarked")

        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs.get('project_id'))

class PositionUpdateView(generics.UpdateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionUpdateSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update the total of an existing position.",
        responses={200: PositionUpdateSerializer}
    )
    def put(self, request, *args, **kwargs):
        position = self.get_object()
        if position.project.user != request.user:
            return Response({"detail": "You do not have permission to update this position."}, status=status.HTTP_403_FORBIDDEN)
        return super().put(request, *args, **kwargs)

class PositionDeleteView(generics.DestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete an existing position.",
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        position = self.get_object()
        if position.project.user != request.user:
            return Response({"detail": "You do not have permission to delete this position."}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

class PositionRenewView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Renew a position for a specified number of days.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'days': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of days to extend the position.'),
                'subcategory': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='Subcategories of the position.')
            },
            required=['days']
        ),
        responses={
            200: openapi.Response(description="Position renewed successfully."),
            400: openapi.Response(description="Invalid data."),
            403: openapi.Response(description="Forbidden - User does not have a valid position."),
        }
    )
    def patch(self, request, position_id):
        user = request.user

        if user.user_type not in ["startup"]:
            return Response(
                {"detail": "Only users with 'startup' type can renew positions."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            position = Position.objects.get(id=position_id, position_user=user)
        except Position.DoesNotExist:
            return Response(
                {"detail": "Position not found or not owned by this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        days_to_renew = request.data.get("days", None)
        subcategories = request.data.get("subcategory", None)

        if not days_to_renew or days_to_renew <= 0:
            return Response(
                {"detail": "Invalid number of days for renewal."},
                status=status.HTTP_400_BAD_REQUEST,
            )


        if days_to_renew == 3:
            renewal_cost = POSITION_RENEWAL_COST_3_DAY
        elif days_to_renew == 7:
            renewal_cost = POSITION_RENEWAL_COST_7_DAY
        elif days_to_renew == 10:
            renewal_cost = POSITION_RENEWAL_COST_10_DAY
        else:
            renewal_cost = POSITION_CREATION_COST_PER_DAY * days_to_renew

        mixin = UserBalanceMixin()
        try:
            mixin.reduce_balance(user, renewal_cost)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        position.end_time += timedelta(days=days_to_renew)
        if subcategories:
            position.subcategory = subcategories  
        position.save()

        return Response(
            {"detail": "Position renewed successfully.", "position": PositionSerializer(position).data},
            status=status.HTTP_200_OK
        )


class PositionCostView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve the position costs.",
        responses={ 
            200: openapi.Response(
                description="Position costs.",
                examples={ 
                    "application/json": {
                        "POSITION_CREATION_BASE_COST": 100000,
                        "POSITION_CREATION_COST_PER_DAY": 10000,
                        "POSITION_RENEWAL_COST_3_DAY": 25000,
                        "POSITION_RENEWAL_COST_7_DAY": 50000,
                        "POSITION_RENEWAL_COST_10_DAY": 80000
                    }
                }
            )
        }
    )
    def get(self, request):
        return Response({
            "POSITION_CREATION_BASE_COST": POSITION_CREATION_BASE_COST,
            "POSITION_CREATION_COST_PER_DAY": POSITION_CREATION_COST_PER_DAY,
            "POSITION_RENEWAL_COST_3_DAY": POSITION_RENEWAL_COST_3_DAY,
            "POSITION_RENEWAL_COST_7_DAY": POSITION_RENEWAL_COST_7_DAY,
            "POSITION_RENEWAL_COST_10_DAY": POSITION_RENEWAL_COST_10_DAY
        })
    
from django.shortcuts import get_object_or_404
from decimal import Decimal

class PositionDetailView(RetrieveAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

from django.utils.dateparse import parse_datetime

class PositionExtendView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Extend the end time of a position.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'end_time': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='New end time for the position.')
            },
            required=['end_time']
        ),
        responses={
            200: openapi.Response(description="Position extended successfully."),
            400: openapi.Response(description="Invalid data or insufficient balance."),
            403: openapi.Response(description="Forbidden - User does not have a valid position."),
        }
    )
    def patch(self, request, position_id):
        user = request.user
        new_end_time_str = request.data.get("end_time")
        new_end_time = parse_datetime(new_end_time_str)

        if not new_end_time:
            return Response({"detail": "Invalid end time format."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            position = Position.objects.get(id=position_id, project__user=user)
        except Position.DoesNotExist:
            return Response({"detail": "Position not found or not owned by this user."}, status=status.HTTP_404_NOT_FOUND)

        if new_end_time <= position.end_time:
            return Response({"detail": "New end time must be after the current end time."}, status=status.HTTP_400_BAD_REQUEST)

        days_to_extend = (new_end_time - position.end_time).days
        cost = 15000 * days_to_extend

        if user.balance < cost:
            return Response({"detail": f"Insufficient balance. You need {cost - user.balance} more."}, status=status.HTTP_400_BAD_REQUEST)

        mixin = UserBalanceMixin()
        try:
            mixin.reduce_balance(user, cost)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        position.end_time = new_end_time
        position.save()

        return Response({"detail": "Position extended successfully.", "position": PositionSerializer(position).data}, status=status.HTTP_200_OK)
