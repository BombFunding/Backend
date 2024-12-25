from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBaseUser
from authenticator.models import BasicUser, StartupUser
from startup.models import StartupProfile
from .serializers import PromotionSerializer
from balance.serializers import change_balance

from drf_yasg.utils import swagger_auto_schema
import drf_yasg.openapi

STARTUP_PROMOTION_COST = 0

class PromotionToStartupView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsBaseUser]
    serializer_class = PromotionSerializer

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
        change_balance(user, -STARTUP_PROMOTION_COST)
        user.user_type = "startup"
        BasicUser.objects.filter(username=user).delete()
        new_startup_user = StartupUser.objects.create(username=user)
        StartupProfile.objects.create(
            startup_user=new_startup_user,
            startup_starting_date=None,
        )
        user.save()
        return Response({"message": "Promotion to startup successful"})