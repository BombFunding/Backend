from django.db.models import Sum
from django.shortcuts import render
from django.db import models
from authenticator.models import BaseUser, StartupUser,BaseProfile
from startup.models import Position , StartupProfile , StartupUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

@api_view(["GET"])
@permission_classes([AllowAny])
def top_liked_startups(request):
    top_startups = (
        StartupProfile.objects.select_related('startup_user__username')
        .order_by('-score')[:10]
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
            "score": startup.score,  
        })

    return Response(data)

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
            "visit_count": startup.startup_profile_visit_count,  
        })

    return Response(data)

@api_view(["GET"])
@permission_classes([AllowAny])
def top_funded_startups(request):
    positions = Position.objects.values('position_user').annotate(
        total_funded=Sum('funded')
    ).order_by('-total_funded')  

    top_users = []
    for position_data in positions[:10]:  
        total_funded = position_data['total_funded']
        profile_picture = None
        user_id = position_data['position_user']  

        
        try:
            user = BaseUser.objects.get(id=user_id, user_type="startup")
        except BaseUser.DoesNotExist:
            continue  

        username = user.username  

        
        try:
            base_profile = BaseProfile.objects.get(base_user=user_id)
            if base_profile.profile_picture:
                profile_picture = base_profile.profile_picture.url
        except BaseProfile.DoesNotExist:
            profile_picture = None

        
        top_users.append({
            "username": username,
            "profile_picture": profile_picture,
            "total_funded": total_funded,
        })

    return Response(top_users)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_statistics(request):
    total_base_profiles = BaseProfile.objects.count()
    total_startup_profiles = StartupProfile.objects.count()
    total_positions = Position.objects.count()

    data = {
        "total_base_profiles": total_base_profiles,
        "total_startup_profiles": total_startup_profiles,
        "total_positions": total_positions,
    }

    return Response(data, status=200)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from position.models import Position
from project.models import CATEGORIES

class CategoryFunded(APIView):
    def get(self, request, *args, **kwargs):
        category_revenue = {category: 0 for category in CATEGORIES.keys()}

        positions = Position.objects.all()

        for position in positions:
            for category, subcategories in CATEGORIES.items():
                if any(subcategory in position.project.subcategories for subcategory in subcategories):
                    category_revenue[category] += position.funded

        return Response(category_revenue, status=status.HTTP_200_OK)
