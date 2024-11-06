from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import StartupProfile, StartupUser
from .serializers import StartupProfileSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # تنها کاربران وارد شده می‌توانند درخواست دهند
def create_startup(request):
    user = request.user

    # بررسی نوع کاربر
    if user.user_type != 'startup':  
        return Response({"detail": "Only users with 'startup' type can create a startup."},
                        status=status.HTTP_403_FORBIDDEN)

    # اطمینان از وجود کاربر 'startup' در جدول StartupUser
    try:
        startup_user = StartupUser.objects.get(username=user)  # جستجو در جدول StartupUser
    except StartupUser.DoesNotExist:
        return Response({"detail": "No related startup found."}, status=status.HTTP_404_NOT_FOUND)

    # ساخت استارتاپ برای کاربر
    serializer = StartupProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(startup_user=startup_user)  # ارتباط دادن استارتاپ به کاربر نوع 'startup'
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
