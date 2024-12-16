from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBaseUser
from authenticator.models import BasicUser, StartupUser, InvestorUser
from startup.models import StartupProfile

from drf_yasg.utils import swagger_auto_schema
import drf_yasg.openapi

class PromotionToStartupView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsBaseUser]

    @swagger_auto_schema(
        operation_description="Promote a basic user to a startup user",
        responses={
            200: drf_yasg.openapi.Schema(
                type=drf_yasg.openapi.TYPE_OBJECT,
                properties={"message": drf_yasg.openapi.Schema(type=drf_yasg.openapi.TYPE_STRING)},
            ),
        },
    )
    def post(self, request):
        user = request.user
        BasicUser.objects.filter(username=user).delete()
        new_startup_user = StartupUser.objects.create(username=user)
        StartupProfile.objects.create(
            startup_user=new_startup_user,
            startup_starting_date=None,
            startup_ending_date=None,
        )
        return Response({"message": "Promotion to startup successful"})

class PromotionToInvestorView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsBaseUser]
    
    @swagger_auto_schema(
        operation_description="Promote a basic user to an investor user",
        responses={
            200: drf_yasg.openapi.Schema(
                type=drf_yasg.openapi.TYPE_OBJECT,
                properties={"message": drf_yasg.openapi.Schema(type=drf_yasg.openapi.TYPE_STRING)},
            ),
        },
    )
    def post(self, request):
        user = request.user
        BasicUser.objects.filter(username=user).delete()
        new_investor_user = InvestorUser.objects.create(username=user)
        return Response({"message": "Promotion to investor successful"})