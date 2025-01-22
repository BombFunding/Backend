
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Pin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PinSerializer
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PinCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    @swagger_auto_schema(
        operation_description="Create a new pin for the authenticated user",
        request_body=PinSerializer,
        responses={
            201: PinSerializer,  
            400: "Bad Request",  
            401: "Unauthorized",  
            500: "Internal Server Error"  
        }
    )
    def post(self, request):
        
        user = request.user
        
        
        serializer = PinSerializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save(user=user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PinListView(APIView):
    permission_classes = [permissions.AllowAny]  

    def get(self, request):
        pins = Pin.objects.all()
        serializer = PinSerializer(pins, many=True)
        return Response(serializer.data)
