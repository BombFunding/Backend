
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from map.models import Pin
from map.serializers import PinSerializer


class PinListView(APIView):
    permission_classes = [permissions.AllowAny]  

    @swagger_auto_schema(
        operation_description="List all pins with detailed user info",
        responses={200: PinSerializer(many=True)}
    )
    def get(self, request):
        pins = Pin.objects.all()
        serializer = PinSerializer(pins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class PinCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    @swagger_auto_schema(
        operation_description="Create a new pin (startup users only, one pin per user)",
        request_body=PinSerializer,
        responses={
            201: PinSerializer,
            400: "Bad Request",
            403: "Forbidden - Only startup users can add pins or user already has a pin."
        }
    )
    def post(self, request):
        user = request.user

        
        if user.user_type != "startup":
            return Response(
                {"detail": "Only startup users can add pins."},
                status=status.HTTP_403_FORBIDDEN
            )

        
        if Pin.objects.filter(user=user).exists():
            return Response(
                {"detail": "You can only add one pin."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
