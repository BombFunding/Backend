from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({"email": user.email, "name": user.name, "user_type": user.user_type}, status=status.HTTP_200_OK)