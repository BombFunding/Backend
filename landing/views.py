from django.shortcuts import render
from django.db import models
from authenticator.models import BaseUser, StartupUser,BaseProfile
from startup.models import StartupApplication , StartupProfile , StartupUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
# پربازدید ترین
# محبوب ترین
# بیشترین درآمد

@api_view(["GET"])
@permission_classes([AllowAny])
def top_visited_startups(request):
    top_startups = (
        StartupProfile.objects.select_related('startup_user__username')
        .order_by('-startup_profile_visit_count')[:10]
    )

    data = [
        {
            "name": startup.startup_user.username.username,
            "profile_picture": startup.startup_user.username.profile_picture.url if hasattr(startup.startup_user.username, 'profile_picture') else None,
        }
        for startup in top_startups
    ]

    return Response(data)