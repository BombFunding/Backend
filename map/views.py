
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from map.models import Pin
from map.serializers import PinSerializer
from django.db import models

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Pin
from collections import defaultdict

def get_province_from_coords(latitude, longitude):
    geolocator = Nominatim(user_agent="YourAppName/1.0 (contact@yourdomain.com)")
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        if location:
            address = location.raw.get('address', {})
            province = address.get('state', address.get('city', None))
            
            if province:
                province = province.replace("استان ", "")
                
                if "خراسان رضوی" in province:
                    province = province.replace("خراسان رضوی", "خ رضوی")
                elif "خراسان جنوبی" in province:
                    province = province.replace("خراسان جنوبی", "خ جنوبی")
                elif "سیستان" in province:
                    province = "سیستان"

            return province
    except GeocoderTimedOut:
        return get_province_from_coords(latitude, longitude)  
    
    return None


class ProvincePinCountView(APIView):
    def get(self, request, *args, **kwargs):
        province_count = defaultdict(int)

        pins = Pin.objects.all()

        for pin in pins:
            province = get_province_from_coords(pin.latitude, pin.longitude)
            if province:
                province_count[province] += 1

        response_data = [{"province": province, "pin_count": count} for province, count in province_count.items()]
        
        return JsonResponse(response_data, safe=False)

    
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


class PinDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]  

    def delete(self, request):
        user = request.user

        pins = Pin.objects.filter(user=user)
        if pins.exists():
            pins.delete()
            return Response({"detail": "All pins deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({"detail": "No pins found for this user."}, status=status.HTTP_200_OK)


User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def user_details(request):
    user = request.user 
    return Response({
        "username": user.username,
        "email": user.email
    })

