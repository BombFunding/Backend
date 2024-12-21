from django.utils import timezone
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import Position, Transaction
from .serializers import PositionSerializer
from rest_framework import mixins, generics, status
from rest_framework.response import Response
from authenticator.models import BaseUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, generics
from drf_yasg import openapi
from datetime import timedelta  
from rest_framework.exceptions import ValidationError 
from balance.utils import UserBalanceMixin
from rest_framework.views import APIView


POSITION_CREATION_BASE_COST = 100000
POSITION_CREATION_COST_PER_DAY = 10000
POSITION_RENEWAL_COST_3_DAY = 25000
POSITION_RENEWAL_COST_7_DAY = 50000
POSITION_RENEWAL_COST_10_DAY = 80000


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
                            "end_time": "2024-12-31T18:00:00Z",
                            "subcategory": "Technology"
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
                            "end_time": "2024-12-15T18:00:00Z",
                            "subcategory": "Energy"
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
            subcategory = serializer.validated_data.get("subcategory")

            # Ensure subcategory is provided
            if not subcategory:
                return Response(
                    {"detail": "Subcategory is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            delta = (end_time - start_time).days
            if delta < 1:  
                return Response(
                    {"detail": "The duration must be at least 1 day."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            mixin = UserBalanceMixin()
            mixin.reduce_balance(user, POSITION_CREATION_COST_PER_DAY * delta + POSITION_CREATION_BASE_COST)

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
                'subcategory': openapi.Schema(type=openapi.TYPE_STRING, description='Subcategory of the position.')
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

        if user.user_type not in ["startup", "investor"]:
            return Response(
                {"detail": "Only users with 'startup' or 'investor' type can renew positions."},
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
        subcategory = request.data.get("subcategory", None)

        if not days_to_renew or days_to_renew <= 0:
            return Response(
                {"detail": "Invalid number of days for renewal."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure subcategory is provided
        if not subcategory:
            return Response(
                {"detail": "Subcategory is required."},
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
        position.subcategory = subcategory  # Update subcategory
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

class InvestmentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create an investment transaction where an investor invests in a position.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'position_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'investment_amount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL)
            }
        ),
        responses={200: openapi.Response(description="Investment successful.")},
    )
    def post(self, request):
        investor = request.user
        position_id = request.data.get("position_id")
        investment_amount = Decimal(request.data.get("investment_amount"))

        if not position_id or investment_amount <= 0:
            return Response(
                {"detail": "Invalid data. Position ID and investment amount are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        position = get_object_or_404(Position, id=position_id)

        if investor.balance < investment_amount:
            return Response(
                {"detail": "Insufficient balance for investment."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if position.position_user == investor:
            return Response(
                {"detail": "You cannot invest in your own position."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if position.is_done:
            return Response(
                {"detail": "This position is already closed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if position.total - position.funded < investment_amount:
            return Response(
                {"detail": "The investment amount exceeds the remaining funding."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if position.end_time < timezone.now():
            return Response(
                {"detail": "This position has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if position.total == position.funded + investment_amount:
            position.is_done = True
            position.save()

        investor.balance -= investment_amount
        investor.save()

        position.position_user.balance += investment_amount
        position.position_user.save()

        position.funded += investment_amount
        position.save()

        transaction = Transaction.objects.create(
            investor_user=investor,
            position=position,
            investment_amount=investment_amount
        )

        return Response(
            {"detail": "Investment successful.", "transaction": {
                "investor": investor.username,
                "position": position.name,
                "investment_amount": str(investment_amount),
                "investment_date": transaction.investment_date
            }},
            status=status.HTTP_201_CREATED
        )
