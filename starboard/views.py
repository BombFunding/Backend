from django.db.models import Sum
from authenticator.models import BaseUser, BaseProfile
from startup.models import Position, StartupProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



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


@swagger_auto_schema(
    method="get",
    manual_parameters=[type_param, results_per_page_param, page_number_param],
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
@api_view(["GET"])
@permission_classes([AllowAny])
def get_top_startups(request):
    top_type = request.GET.get("type")  
    results_per_page = int(request.GET.get("results_per_page", 10))
    page_number = int(request.GET.get("page_number", 1))

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

            data.append({
                "username": username,
                "profile_picture": profile_picture,
                "total_funded": total_funded,
            })

    else:
        return Response({"error": "'type' must be 'top_liked', 'top_visited', or 'top_funded'."}, status=400)

    return Response(data)
