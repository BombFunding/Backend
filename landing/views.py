from django.db.models import Sum
from django.shortcuts import render
from django.db import models
from authenticator.models import BaseUser, StartupUser,BaseProfile
from startup.models import StartupApplication , StartupProfile , StartupUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes


from django.db.models import Sum
from django.shortcuts import render
from django.db import models
from authenticator.models import BaseUser, StartupUser, BaseProfile
from startup.models import StartupApplication, StartupProfile, StartupUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

@api_view(["GET"])
@permission_classes([AllowAny])
def top_visited_startups(request):
    top_startups = (
        StartupProfile.objects.select_related('startup_user__username')
        .order_by('-startup_profile_visit_count')[:10]
    )

    data = []

    for startup in top_startups:
        username = startup.startup_user.username.username
        profile_picture = None

        try:
            base_profile = BaseProfile.objects.get(base_user__username=username)
            if base_profile.profile_picture:
                profile_picture = base_profile.profile_picture.url
        except BaseProfile.DoesNotExist:
            profile_picture = None

        data.append({
            "username": username,
            "profile_picture": profile_picture,
        })

    return Response(data)
