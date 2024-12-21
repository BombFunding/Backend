from django.db.models import Sum
from django.shortcuts import render
from django.db import models
from authenticator.models import BaseUser, StartupUser, BaseProfile
from startup.models import Position, StartupProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method="post",
    operation_description="Retrieve startups based on the specified 'type' ('top_liked', 'top_visited', 'top_funded') and pagination details.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'type': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Type of the top startups to retrieve: 'top_liked', 'top_visited', or 'top_funded'."
            ),
            'results_per_page': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Number of results per page",
                default=10
            ),
            'page_number': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Page number to retrieve",
                default=1
            ),
        },
        required=['type']
    ),
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                    'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, format='uri', description="URL of the profile picture"),
                    'score': openapi.Schema(type=openapi.TYPE_INTEGER, description="Score of the startup (for top_liked)"),
                    'visit_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Visit count of the startup (for top_visited)"),
                    'total_funded': openapi.Schema(type=openapi.TYPE_INTEGER, description="Total funded amount (for top_funded)"),
                },
            ),
        ),
        400: "Invalid request"
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def get_top_startups(request):
    top_type = request.data.get("type")
    results_per_page = request.data.get("results_per_page", 10)
    page_number = request.data.get("page_number", 1)

    if not top_type:
        return Response({"error": "'type' parameter is required."}, status=400)

    
    start_index = (page_number - 1) * results_per_page
    end_index = start_index + results_per_page

    data = []

    if top_type == "top_liked":
        top_startups = (
            StartupProfile.objects.select_related('startup_user__username')
            .order_by('-score')[start_index:end_index]
        )

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

    elif top_type == "top_visited":
        top_startups = (
            StartupProfile.objects.select_related('startup_user__username')
            .order_by('-startup_profile_visit_count')[start_index:end_index]
        )

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

    elif top_type == "top_funded":
        positions = Position.objects.values('position_user').annotate(
            total_funded=Sum('funded')
        ).order_by('-total_funded')[start_index:end_index]

        for position_data in positions:
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

            data.append({
                "username": username,
                "profile_picture": profile_picture,
                "total_funded": total_funded,
            })

    else:
        return Response({"error": "'type' must be 'top_liked', 'top_visited', or 'top_funded'."}, status=400)

    return Response(data)
