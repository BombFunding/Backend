from django.db.models import Sum
from django.shortcuts import render
from django.db import models
from authenticator.models import BaseUser, StartupUser, BaseProfile
from startup.models import StartupProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method="post",
    operation_description="Retrieve startups based on the specified 'top' type (e.g., 'top_liked', 'top_visited', 'top_funded') and pagination details.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'top': openapi.Schema(
                type=openapi.TYPE_STRING,
                description="The type of top startups to retrieve ('top_liked', 'top_visited', 'top_funded')",
            ),
            'results_per_page': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Number of results per page",
            ),
            'page_number': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Page number to retrieve",
            ),
        },
        required=['top']
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
def top_startups(request):
    top_type = request.data.get("top")
    results_per_page = request.data.get("results_per_page", 10)
    page_number = request.data.get("page_number", 1)

    if not top_type:
        return Response({"error": "Invalid request. 'top' parameter is required."}, status=400)

    if top_type == "top_liked":
        top_startups = (
            StartupProfile.objects.select_related('startup_user__username')
            .order_by('-score')
        )
        data_key = "score"
        value_key = "score"

    elif top_type == "top_visited":
        top_startups = (
            StartupProfile.objects.select_related('startup_user__username')
            .order_by('-startup_profile_visit_count')
        )
        data_key = "visit_count"
        value_key = "startup_profile_visit_count"

    elif top_type == "top_funded":
        startup_funding_data = []

        for startup in StartupProfile.objects.all():
            total_funded = startup.positions.aggregate(
                funded_sum=models.Sum('funded')
            )['funded_sum'] or 0

            startup_funding_data.append({
                "startup": startup,
                "total_funded": total_funded,
            })

        startup_funding_data = sorted(
            startup_funding_data,
            key=lambda x: x['total_funded'],
            reverse=True
        )

        start_index = (page_number - 1) * results_per_page
        end_index = start_index + results_per_page
        top_startups = startup_funding_data[start_index:end_index]

        data_key = "total_funded"
        value_key = "total_funded"

    else:
        return Response({"error": "Invalid 'top' value."}, status=400)

    if top_type != "top_funded":
        start_index = (page_number - 1) * results_per_page
        end_index = start_index + results_per_page
        top_startups = top_startups[start_index:end_index]

    data = []

    for startup_entry in top_startups:
        if top_type == "top_funded":
            startup = startup_entry['startup']
            value = startup_entry['total_funded']
        else:
            startup = startup_entry
            value = getattr(startup, value_key, None)

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
            data_key: value,
        })

    return Response(data)
