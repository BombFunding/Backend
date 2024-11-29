from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext as _

from startup.PersianSwear import PersianSwear

from .models import (
    StartupComment,
    StartupPosition,
    StartupProfile,
    StartupUser,
)
from .serializers import (
    StartupCommentSerializer,
    StartupPositionSerializer,
    StartupProfileSerializer,
)


@api_view(["GET"])
@permission_classes([AllowAny])
def sort_positions_by_funded(request):
    order = request.query_params.get("order", "asc")
    if order == "asc":
        positions = StartupPosition.objects.all().order_by("funded")
    else:
        positions = StartupPosition.objects.all().order_by("-funded")

    result = [
        {
            "name": pos.name,
            "bio": pos.bio,
            "total": pos.total,
            "funded": pos.funded,
            "is_done": pos.is_done,
            "start_time": pos.start_time,
            "end_time": pos.end_time,
        }
        for pos in positions
    ]

    return JsonResponse({"positions": result}, safe=False)


@api_view(["GET"])
@permission_classes([AllowAny])
def sort_positions_by_date(request):
    order = request.query_params.get("order", "asc")
    if order == "asc":
        positions = StartupPosition.objects.all().order_by("start_time")
    else:
        positions = StartupPosition.objects.all().order_by("-start_time")

    result = [
        {
            "name": pos.name,
            "bio": pos.bio,
            "total": pos.total,
            "funded": pos.funded,
            "is_done": pos.is_done,
            "start_time": pos.start_time,
            "end_time": pos.end_time,
        }
        for pos in positions
    ]

    return JsonResponse({"positions": result}, safe=False)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_positions(request):
    try:
        positions = StartupPosition.objects.all()
        result = [
            {
                "id": pos.id,
                "name": pos.name,
                "bio": pos.bio,
                "total": pos.total,
                "funded": pos.funded,
                "is_done": pos.is_done,
                "start_time": pos.start_time,
                "end_time": pos.end_time,
                "startup_profile": {
                    "startup_profile_id": pos.startup_profile.id,
                    "name": pos.startup_profile.name,
                },
            }
            for pos in positions
        ]

        return JsonResponse({"positions": result}, safe=False)

    except Exception as e:
        return JsonResponse({"error": _("Error: ") + str(e)}, status=500)


@api_view(["GET"])
@permission_classes([AllowAny])
def search_positions_by_date_range(request):
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")

    if not start_date or not end_date:
        return JsonResponse(
            {"error": _("Both 'start_date' and 'end_date' are required.")}, status=400
        )

    parsed_start_date = parse_datetime(start_date + "T00:00:00Z")
    parsed_end_date = parse_datetime(end_date + "T23:59:59Z")

    if not parsed_start_date or not parsed_end_date:
        return JsonResponse(
            {"error": _("Invalid date format. Use YYYY-MM-DD.")}, status=400
        )

    positions = StartupPosition.objects.filter(
        end_time__gte=parsed_start_date, end_time__lte=parsed_end_date
    )

    result = [
        {
            "name": pos.name,
            "bio": pos.bio,
            "total": pos.total,
            "funded": pos.funded,
            "is_done": pos.is_done,
            "start_time": pos.start_time,
            "end_time": pos.end_time,
        }
        for pos in positions
    ]

    return JsonResponse({"positions": result}, safe=False)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_update_position(request):
    user = request.user

    if user.user_type != "startup":
        return Response(
            {
                str(_("error")): _("Only users with type 'startup' can create or update startup positions.")
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        startup_user = StartupUser.objects.get(username=user)
    except StartupUser.DoesNotExist:
        return Response(
            {str(_("error")): _("Related startup not found.")}, status=status.HTTP_404_NOT_FOUND
        )

    try:
        startup_profile = StartupProfile.objects.get(startup_user=startup_user)
    except StartupProfile.DoesNotExist:
        startup_profile = StartupProfile.objects.create(
            startup_user=startup_user, name="Default Name", bio="Default bio"
        )

    position_name = request.data.get("name")
    try:
        position = StartupPosition.objects.get(
            startup_profile=startup_profile, name=position_name
        )

        serializer = StartupPositionSerializer(
            position, data=request.data, partial=True
        )
        message = "Position successfully updated."
    except StartupPosition.DoesNotExist:
        serializer = StartupPositionSerializer(data=request.data)
        message = "Position successfully created."

    if serializer.is_valid():
        serializer.save(startup_profile=startup_profile)
        return Response(
            {str(_("message")): _("Position successfully updated."), "position": serializer.data}, status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_comments_by_profile(request, profile_id):
    try:
        comments = StartupComment.objects.filter(
            startup_profile__id=profile_id
        ).order_by("-time")

        if not comments.exists():
            return JsonResponse(
                {str(_("error")): _("No comments found for this profile.")}, status=404
            )

        serializer = StartupCommentSerializer(comments, many=True)

        comments_with_id = []
        for comment in serializer.data:
            comment.pop("startup_profile", None)
            comment["id"] = comment.get("id", None)
            comments_with_id.append(comment)

        return JsonResponse(
            {"comments": comments_with_id},
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    except Exception as e:
        return JsonResponse({str(_("error")): _("Error: ") + str(e)}, status=500)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    try:
        comment = StartupComment.objects.get(id=comment_id)
    except StartupComment.DoesNotExist:
        return Response(
            {str(_("error")): _("Comment not found.")}, status=status.HTTP_404_NOT_FOUND
        )

    if comment.username != request.user:
        return Response(
            {str(_("error")): _("You do not have permission to delete this comment.")},
            status=status.HTTP_403_FORBIDDEN,
        )

    comment.delete()

    return Response(
        {str(_("message")): _("Comment successfully deleted.")}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_comment(request, profile_id):
    try:
        startup_profile = StartupProfile.objects.get(id=profile_id)
    except StartupProfile.DoesNotExist:
        return Response(
            {str(_("error")): _("Startup profile not found.")}, status=status.HTTP_404_NOT_FOUND
        )

    user = request.user
    comment = request.data.get("comment")

    persianswear = PersianSwear()
    if not comment:
        return Response(
            {str(_("error")): _("Comment is required.")}, status=status.HTTP_400_BAD_REQUEST
        )
    if persianswear.has_swear(comment):
        return Response(
            {str(_("error")): _("Comment contains inappropriate language.")},
            status=status.HTTP_400_BAD_REQUEST,
        )

    new_comment = StartupComment.objects.create(
        startup_profile=startup_profile,
        username=user,
        comment=comment,
        time=timezone.now(),
    )

    serializer = StartupCommentSerializer(new_comment)
    return Response(
        {
            str(_("message")): _("Comment successfully added."),
            "comment": {"id": new_comment.id, **serializer.data},
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_comment(request, comment_id):
    try:
        comment = StartupComment.objects.get(id=comment_id)
    except StartupComment.DoesNotExist:
        return Response(
            {str(_("error")): _("Comment not found.")}, status=status.HTTP_404_NOT_FOUND
        )

    if comment.username != request.user:
        return Response(
            {str(_("error")): _("You do not have permission to edit this comment.")},
            status=status.HTTP_403_FORBIDDEN,
        )

    updated_comment = request.data.get("comment")
    if not updated_comment:
        return Response(
            {str(_("error")): _("New comment text is required.")},
            status=status.HTTP_400_BAD_REQUEST,
        )

    persianswear = PersianSwear()
    if persianswear.has_swear(updated_comment):
        return Response(
            {str(_("error")): _("Comment contains inappropriate language.")},
            status=status.HTTP_400_BAD_REQUEST,
        )

    comment.comment = updated_comment
    comment.save()

    return Response(
        {str(_("message")): _("Comment successfully updated.")}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def startup_search_by_name(request, username):
    try:
        startup_user = StartupUser.objects.get(username__username=username)
        startup_profile = StartupProfile.objects.get(startup_user=startup_user)

        positions = StartupPosition.objects.filter(startup_profile=startup_profile)
        positions_data = [
            {
                "name": position.name,
                "bio": position.bio,
                "total": position.total,
                "funded": position.funded,
                "is_done": position.is_done,
                "start_time": position.start_time,
                "end_time": position.end_time,
            }
            for position in positions
        ]

        return Response(
            {
                "startup_profile": {
                    "name": startup_profile.name,
                    "bio": startup_profile.bio,
                    "page": startup_profile.page,
                    "categories": startup_profile.categories,
                    "email": startup_user.username.email,
                    "socials": startup_profile.socials,
                    "first_name": startup_profile.first_name,
                    "last_name": startup_profile.last_name,
                    "profile_picture": (
                        startup_profile.profile_picture.url
                        if startup_profile.profile_picture
                        else None
                    ),
                    "header_picture": (
                        startup_profile.header_picture.url
                        if startup_profile.header_picture
                        else None
                    ),
                },
                "positions": positions_data,
            },
            status=status.HTTP_200_OK,
        )

    except StartupUser.DoesNotExist:
        return Response(
            {str(_("error")): _("Startup user not found.")}, status=status.HTTP_404_NOT_FOUND
        )
    except StartupProfile.DoesNotExist:
        return Response(
            {str(_("error")): _("Startup profile not found.")}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({str(_("error")): str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_own_startup_profile(request):
    user = request.user
    try:
        startup_user = StartupUser.objects.get(username=user)
        startup_profile = StartupProfile.objects.get(startup_user=startup_user)

        positions = StartupPosition.objects.filter(startup_profile=startup_profile)
        positions_data = [
            {
                "name": position.name,
                "bio": position.bio,
                "total": position.total,
                "funded": position.funded,
                "is_done": position.is_done,
                "start_time": position.start_time,
                "end_time": position.end_time,
            }
            for position in positions
        ]

        return Response(
            {
                "startup_profile": {
                    "name": startup_profile.name,
                    "bio": startup_profile.bio,
                    "page": startup_profile.page,
                    "categories": startup_profile.categories,
                    "email": user.email,
                    "socials": startup_profile.socials,
                    "phone": startup_profile.phone,
                    "first_name": startup_profile.first_name,
                    "last_name": startup_profile.last_name,
                    "profile_picture": (
                        startup_profile.profile_picture.url
                        if startup_profile.profile_picture
                        else None
                    ),
                    "header_picture": (
                        startup_profile.header_picture.url
                        if startup_profile.header_picture
                        else None
                    ),
                },
                "positions": positions_data,
            },
            status=status.HTTP_200_OK,
        )

    except StartupUser.DoesNotExist:
        return Response(
            {str(_("error")): _("Startup user not found.")}, status=status.HTTP_404_NOT_FOUND
        )
    except StartupProfile.DoesNotExist:
        return Response(
            {str(_("error")): _("Startup profile not found.")}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({str(_("error")): str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_startup_profile(request):
    user = request.user

    if user.user_type != "startup":
        return Response(
            {
                str(_("error")): _("Only users with type 'startup' can create or update startup profiles.")
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        startup_user = StartupUser.objects.get(username=user)
    except StartupUser.DoesNotExist:
        return Response(
            {str(_("error")): _("Related startup not found.")}, status=status.HTTP_404_NOT_FOUND
        )

    profile = StartupProfile.objects.filter(startup_user=startup_user).first()

    if profile:
        non_editable_fields = ["name", "email"]
        data = {
            key: value
            for key, value in request.data.items()
            if key not in non_editable_fields
        }
        serializer = StartupProfileSerializer(profile, data=data, partial=True)
        message = "Profile successfully updated."
    else:
        serializer = StartupProfileSerializer(data=request.data)
        message = "Profile successfully created."

    if serializer.is_valid():
        serializer.save(startup_user=startup_user)
        return Response(
            {
                str(_("message")): _(message),
                "profile": {
                    "username": user.username,
                    "email": user.email,
                    **serializer.data,
                    "profile_picture": (
                        profile.profile_picture.url
                        if profile and profile.profile_picture
                        else None
                    ),
                    "header_picture": (
                        profile.header_picture.url
                        if profile and profile.header_picture
                        else None
                    ),
                },
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
