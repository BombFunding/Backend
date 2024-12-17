from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import BalanceSerializer


class BalanceUpdateView(generics.GenericAPIView):
    serializer_class = BalanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update the balance of the authenticated user",
        request_body=BalanceSerializer,
        responses={
            200: openapi.Response(
                description="Balance updated",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "balance": openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Balance after upadating",
                        ),
                    },
                ),
            ),
            400: "Bad Request",
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response(
                {"message": "balance updated", "balance": user.balance},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Get the balance of the authenticated user",
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({"balance": user.balance}, status=status.HTTP_200_OK)