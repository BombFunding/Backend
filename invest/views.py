from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from decimal import Decimal
from rest_framework.exceptions import ValidationError
from balance.utils import UserBalanceMixin
from .models import Transaction
from .serializers import TransactionSerializer, ProjectInvestmentHistorySerializer
from position.models import Position
from drf_yasg import openapi
from notifications.models import send_investment_notification


class InvestmentCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create an investment transaction where an investor invests in a position.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'investment_amount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL)
            },
            required=['investment_amount']
        ),
        responses={200: openapi.Response(description="Investment successful.")},
    )
    def post(self, request, *args, **kwargs):
        investor = request.user
        position_id = kwargs.get('position_id')
        investment_amount = Decimal(request.data.get("investment_amount"))

        if investment_amount <= 0:
            return Response(
                {"detail": "Invalid data. Investment amount must be greater than 0."},
                status=status.HTTP_400_BAD_REQUEST
            )

        position = get_object_or_404(Position, id=position_id)
        position_owner = position.project.user

        if investor.balance < investment_amount:
            return Response(
                {"detail": "Insufficient balance for investment."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if position_owner == investor:
            return Response(
                {"detail": "You cannot invest in your own position."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if position.is_closed:
            return Response(
                {"detail": "This position is already closed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        investor.balance -= investment_amount
        investor.save()

        position_owner.balance += investment_amount
        position_owner.save()
        # position_owner.profile.total_funds_received += investment_amount  # Increment the fund for the profile statistics
        # position_owner.profile.save()

        position.funded += investment_amount
        position.save()

        transaction = Transaction.objects.create(
            investor_user=investor,
            position=position,
            investment_amount=investment_amount
        )

        send_investment_notification(investor, position_owner, investment_amount)

        return Response(
            {"detail": "Investment successful.", "transaction": {
                "investor": investor.username,
                "position": position.id,
                "investment_amount": str(investment_amount),
                "investment_date": transaction.investment_date
            }},
            status=status.HTTP_201_CREATED
        )
class InvestmentHistoryView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get investment history for a user, sorted by time or amount",
        manual_parameters=[
            openapi.Parameter(
                'sort', openapi.IN_PATH, 
                description="Sort by 'time' or 'amount'", 
                type=openapi.TYPE_STRING,
                enum=['time', 'amount']
            ),
        ],
        responses={
            200: openapi.Response(description="Investment history retrieved successfully."),
            400: openapi.Response(description="Invalid sort parameter."),
        }
    )
    def get_queryset(self):
        username = self.kwargs['username']
        sort_by = self.kwargs['sort']

        if sort_by not in ['time', 'amount']:
            raise ValidationError("Sort parameter must be either 'time' or 'amount'")

        queryset = Transaction.objects.filter(investor_user__username=username)
        
        if sort_by == 'time':
            return queryset.order_by('-investment_date')
        else:  # sort_by == 'amount'
            return queryset.order_by('-investment_amount')


class ProjectInvestmentHistoryView(generics.ListAPIView):
    serializer_class = ProjectInvestmentHistorySerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get investment history for a specific project",
        responses={
            200: openapi.Response(description="Investment history retrieved successfully."),
            404: openapi.Response(description="Project not found."),
        }
    )
    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Transaction.objects.filter(
            position__project_id=project_id
        ).order_by('-investment_date')


class StartupInvestmentHistoryView(generics.ListAPIView):
    serializer_class = ProjectInvestmentHistorySerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get investment history for all projects owned by a startup",
        responses={
            200: openapi.Response(description="Investment history retrieved successfully."),
            404: openapi.Response(description="Startup not found or has no projects."),
        }
    )
    def get_queryset(self):
        startup_id = self.kwargs['startup_id']
        return Transaction.objects.filter(
            position__project__user_id=startup_id
        ).order_by('-investment_date')
