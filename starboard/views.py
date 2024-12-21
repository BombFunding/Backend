from django.db.models import Sum
from authenticator.models import BaseUser, BaseProfile
from startup.models import Position, StartupProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
from drf_yasg import openapi
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema


type_param = openapi.Parameter(
    'type',
    openapi.IN_QUERY,
    description="Type of the top startups to retrieve: 'top_liked', 'top_visited', or 'top_funded'.",
    type=openapi.TYPE_STRING,
    enum=["top_liked", "top_visited", "top_funded"]  
)

results_per_page_param = openapi.Parameter(
    'results_per_page',
    openapi.IN_QUERY,
    description="Number of results per page",
    type=openapi.TYPE_INTEGER,
    default=10
)

page_number_param = openapi.Parameter(
    'page_number',
    openapi.IN_QUERY,
    description="Page number to retrieve",
    type=openapi.TYPE_INTEGER,
    default=1
)


filter_by_subcategory_param = openapi.Parameter(
    'filter_by_subcategory',
    openapi.IN_QUERY,
    description="Comma-separated list of subcategories to filter the positions by. Example: 'Technology,Art,Health'",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_STRING),
)

@swagger_auto_schema(
    method="get",
    manual_parameters=[type_param, results_per_page_param, page_number_param, filter_by_subcategory_param],
    responses={200: openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                    'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, format='uri', description="URL of the profile picture"),
                    'positions': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'total': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'funded': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'start_time': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                        'end_time': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                    }))
                },
            ),
        ),
    400: "Invalid request"
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def get_top_startups(request):
    top_type = request.GET.get("type")  
    results_per_page = int(request.GET.get("results_per_page", 10))
    page_number = int(request.GET.get("page_number", 1))
    filter_by_subcategory = request.GET.get("filter_by_subcategory")

    if not top_type:
        return Response({"error": "'type' parameter is required."}, status=400)

    try:
        filter_by_subcategory = json.loads(filter_by_subcategory) if filter_by_subcategory else {}
    except json.JSONDecodeError:
        return Response({"error": "'filter_by_subcategory' must be a valid JSON object."}, status=400)

    start_index = (page_number - 1) * results_per_page
    end_index = start_index + results_per_page

    data = []

    if top_type == "top_liked":
        top_startups = (
            StartupProfile.objects.select_related('startup_user')
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

            positions = Position.objects.filter(position_user__username=username)

            valid_positions = []
            for position in positions:
                position_subcategories = set(position.subcategory)
                if set(filter_by_subcategory).issubset(position_subcategories):
                    valid_positions.append({
                        "name": position.name,
                        "description": position.description,
                        "total": position.total,
                        "funded": position.funded,
                        "start_time": position.start_time,
                        "end_time": position.end_time,
                        "subcategory": list(position_subcategories),  
                    })

            if valid_positions:
                data.append({
                    "username": username,
                    "profile_picture": profile_picture,
                    "score": startup.score,
                    "positions": valid_positions,
                })

    elif top_type == "top_visited":
        top_startups = (
            StartupProfile.objects.select_related('startup_user')
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

            positions = Position.objects.filter(position_user__username=username)

            valid_positions = []
            for position in positions:
                position_subcategories = set(position.subcategory)
                if set(filter_by_subcategory).issubset(position_subcategories):
                    valid_positions.append({
                        "name": position.name,
                        "description": position.description,
                        "total": position.total,
                        "funded": position.funded,
                        "start_time": position.start_time,
                        "end_time": position.end_time,
                        "subcategory": list(position_subcategories),  
                    })

            if valid_positions:
                data.append({
                    "username": username,
                    "profile_picture": profile_picture,
                    "visit_count": startup.startup_profile_visit_count,
                    "positions": valid_positions,
                })

    elif top_type == "top_funded":
        funded_data = (
            Position.objects.values('position_user__username')
            .annotate(total_funded=Sum('funded'))
            .order_by('-total_funded')[start_index:end_index]
        )

        for entry in funded_data:
            username = entry['position_user__username']
            total_funded = entry['total_funded']
            profile_picture = None

            try:
                base_profile = BaseProfile.objects.get(base_user__username=username)
                if base_profile.profile_picture:
                    profile_picture = base_profile.profile_picture.url
            except BaseProfile.DoesNotExist:
                profile_picture = None

            positions = Position.objects.filter(position_user__username=username)

            valid_positions = []
            for position in positions:
                position_subcategories = set(position.subcategory)
                if set(filter_by_subcategory).issubset(position_subcategories):
                    valid_positions.append({
                        "name": position.name,
                        "description": position.description,
                        "total": position.total,
                        "funded": position.funded,
                        "start_time": position.start_time,
                        "end_time": position.end_time,
                        "subcategory": list(position_subcategories),  
                    })

            if valid_positions:
                data.append({
                    "username": username,
                    "profile_picture": profile_picture,
                    "total_funded": total_funded,
                    "positions": valid_positions,
                })

    else:
        return Response({"error": "'type' must be 'top_liked', 'top_visited', or 'top_funded'."}, status=400)

    return Response(data)
