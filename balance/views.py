from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import BalanceSerializer


class BalanceUpdateView(generics.GenericAPIView):
    serializer_class = BalanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get the balance of the authenticated user",
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({"balance": user.balance}, status=status.HTTP_200_OK)
