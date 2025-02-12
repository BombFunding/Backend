from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django_email_verification import send_email
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError as RestValidationError
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from .models import BaseUser,BaseProfile,BaseuserComment
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.translation import gettext as _

from .models import BaseUser
from .serializers import (
    EmailSerializer,
    LoginSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
    BaseProfileSerializer,
    BaseuserCommentSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        send_email(user)

        return Response(
            {_("message"): _("User created successfully.")}, status=status.HTTP_201_CREATED
        )


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_description="Login to the application and get tokens to authenticate future requests.",
        responses={200: openapi.Response(_("Login successful")), 400: _("Invalid username or password.")},
        tags=["auth"],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response(
            {
                "email": user.email,
                "username": user.username,
                "user_type": user.user_type,
                "access_token": access_token,
                "refresh_token": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


class ForgetPasswordEmailView(GenericAPIView):
    serializer_class = EmailSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Sends an email to the user with a link to reset their password.",
        request_body=EmailSerializer,
        responses={200: _("Email sent"), 400: _("Email does not exist.")},
        tags=["auth"],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f"http://localhost:3000/reset-password/{uid}/{token}"

        send_mail(
            subject=_("Reset your password"),
            message=_("Click the link below to reset your password.") + reset_url,
            from_email="sendemailviapython3@gmail.com",
            recipient_list=[user.email],
        )

        return Response({_("message"): _("An email has been sent to reset your password.")}, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        try:
            user.change_password(serializer.validated_data["password"])
        except DjangoValidationError as e:
            return Response(
                {_("message"): e.message_dict}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {_("message"): _("Password successfully changed.")}, status=status.HTTP_200_OK
        )


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "new_password": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="The new password for the user.",
                example="SecureNewPassword123!"
            ),
        },
        required=["new_password"],
    ),
    responses={
        200: openapi.Response(
            description="Password successfully changed.",
            examples={
                "application/json": {"message": "Password successfully changed."}
            },
        ),
        400: openapi.Response(
            description="Invalid input or validation error.",
            examples={
                "application/json": {
                    "detail": "New password is required."
                }
            },
        ),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_user_password(request):
    user = request.user
    new_password = request.data.get("new_password")

    if not new_password:
        return Response(
            {_("detail"): _("New password is required.")}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user.change_password(new_password)
    except DjangoValidationError as e:
        return Response(
            {_("message"): e.message_dict}, status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {_("message"): _("Password successfully changed.")}, status=status.HTTP_200_OK
    )

@swagger_auto_schema(
    method="get",
    responses={
        200: openapi.Response(
            description="Baseuser profile found successfully.",
            examples={
                "application/json": {
                    "base_profile": {
                        "name": "admin",
                        "bio": "",
                        "email": "admin@gmail.com",
                        "socials": {},
                        "first_name": None,
                        "last_name": None,
                        "profile_picture": "/media/profile_pics/default_profile.jpg",
                        "header_picture": "/media/header_pics/default_header.jpg"
                    }
                }
            },
        )
    },
)
@api_view(["GET"])
def baseuser_search_by_name(request, username):
    try:
        base_user = BaseUser.objects.get(username=username)
        baseuser_profile = BaseProfile.objects.get(base_user=base_user)

        return Response(
            {
                "baseuser_profile": {
                    "name": baseuser_profile.name,
                    "bio": baseuser_profile.bio,
                    "email": base_user.email, 
                    "socials": baseuser_profile.socials,
                    "user_type": base_user.user_type,
                    "first_name": baseuser_profile.first_name,
                    "last_name": baseuser_profile.last_name,
                    "profile_picture": (
                        baseuser_profile.profile_picture.url
                        if baseuser_profile.profile_picture
                        else None
                    ),
                    "header_picture": (
                        baseuser_profile.header_picture.url
                        if baseuser_profile.header_picture
                        else None
                    ),
                },
            },
            status=status.HTTP_200_OK,
        )

    except BaseUser.DoesNotExist:
        return Response(
            {_("detail"): _("Baseuser user not found.")}, status=status.HTTP_404_NOT_FOUND
        )
    except BaseProfile.DoesNotExist:
        return Response(
            {_("detail"): _("Baseuser profile not found.")}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({_("detail"): str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method="get",
    responses={
        200: openapi.Response(
            description="User profile retrieved successfully.",
            examples={
                "application/json": {
                    "base_profile": {
                        "name": "admin",
                        "bio": "",
                        "email": "admin@gmail.com",
                        "socials": {},
                        "phone": None,
                        "first_name": None,
                        "last_name": None,
                        "profile_picture": "/media/profile_pics/default_profile.jpg",
                        "header_picture": "/media/header_pics/default_header.jpg"
                    }
                }
            },
        ),
        401: openapi.Response(
            description="Authentication credentials were not provided or invalid.",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided."
                }
            },
        ),
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_own_baseuser_profile(request):
    user = request.user
    try:
        base_user = BaseUser.objects.get(username=user.username) 
        base_profile = BaseProfile.objects.get(base_user=base_user)

        return Response(
            {
                "base_profile": {
                    "name": base_profile.name,
                    "bio": base_profile.bio,
                    "email": user.email,
                    "socials": base_profile.socials,
                    "user_type": base_user.user_type,
                    "phone": base_profile.phone,
                    "first_name": base_profile.first_name,
                    "last_name": base_profile.last_name,
                    "profile_picture": (
                        base_profile.profile_picture.url
                        if base_profile.profile_picture
                        else None
                    ),
                    "header_picture": (
                        base_profile.header_picture.url
                        if base_profile.header_picture
                        else None
                    ),
                },
            },
            status=status.HTTP_200_OK,
        )

    except BaseUser.DoesNotExist:
        return Response(
            {_("detail"): _("Base user not found.")}, status=status.HTTP_404_NOT_FOUND
        )
    except BaseProfile.DoesNotExist:
        return Response(
            {_("detail"): _("Base profile not found.")}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({_("detail"): str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "phone": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Phone number of the user",
                example="+0"
            ),
            "first_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="First name of the user",
                example="!"
            ),
            "last_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Last name of the user",
                example="!"
            ),
            "bio": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="A short bio about the user",
                example="!"
            ),
            "page": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Web page and social media links",
                properties={
                    "website": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format="url",
                        description="Website link",
                        example="https://www.newstartup.com"
                    ),
                    "facebook": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format="url",
                        description="Facebook page link",
                        example="https://facebook.com/newstartup"
                    )
                },
            ),
            "categories": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description="List of categories",
                example=["Technology", "AI", "Innovation"]
            ),
            "socials": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Social media links",
                properties={
                    "linkedin": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format="url",
                        description="LinkedIn profile link",
                        example="https://linkedin.com/company/newstartup"
                    ),
                    "twitter": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format="url",
                        description="Twitter profile link",
                        example="https://twitter.com/newstartup"
                    )
                }
            ),
        },
        required=["phone", "first_name", "last_name", "bio", "page", "categories", "socials"],
        example={
            "phone": "+0",
            "first_name": "!",
            "last_name": "!",
            "bio": "!",
            "page": {
                "website": "https://www.newstartup.com",
                "facebook": "https://facebook.com/newstartup"
            },
            "categories": ["Technology", "AI", "Innovation"],
            "socials": {
                "linkedin": "https://linkedin.com/company/newstartup",
                "twitter": "https://twitter.com/newstartup"
            }
        }
    )
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_baseuser_profile(request):
    user = request.user

    try:
        base_user = BaseUser.objects.get(username=user.username)
    except BaseUser.DoesNotExist:
        return Response(
            {_("detail"): _("No related base user found.")}, status=status.HTTP_404_NOT_FOUND
        )

    base_profile = BaseProfile.objects.filter(base_user=base_user).first()

    if base_profile:
        non_editable_fields = ["name", "email"]
        data = {
            key: value
            for key, value in request.data.items()
            if key not in non_editable_fields
        }
        serializer = BaseProfileSerializer(base_profile, data=data, partial=True)
        message = _("Profile updated successfully.")
    else:
        serializer = BaseProfileSerializer(data=request.data)
        message = _("Profile created successfully.")

    if serializer.is_valid():
        serializer.save(base_user=base_user)
        return Response(
            {
                _("detail"): message,
                "profile": {
                    "username": user.username,
                    "email": user.email,
                    **serializer.data,
                },
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_comments_by_profile(request, username):
    try:
        baseuser_profile = BaseProfile.objects.get(base_user__username=username)

        comments = BaseuserComment.objects.filter(
            baseuser_profile=baseuser_profile
        ).order_by("-time")

        if not comments.exists():
            return JsonResponse(
                {_("detail"): _("No comments found for this profile.")}, status=404
            )

        serializer = BaseuserCommentSerializer(comments, many=True)

        comments_with_id = []
        for comment in serializer.data:
            comment.pop("baseuser_profile", None)
            comment["id"] = comment.get("id", None)
            comments_with_id.append(comment)

        return JsonResponse(
            {"comments": comments_with_id},
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    except BaseProfile.DoesNotExist:
        return JsonResponse(
            {_("detail"): _("Baseuser profile not found.")}, status=404
        )
    except Exception as e:
        return JsonResponse({_("detail"): f"Error: {str(e)}"}, status=500)


@swagger_auto_schema(
    method="delete",
    responses={
        200: openapi.Response(
            description="Comment deleted successfully.",
            examples={
                "application/json": {
                    "detail": "Comment deleted successfully."
                }
            }
        ),
        403: openapi.Response(
            description="Permission denied.",
            examples={
                "application/json": {
                    "detail": "You do not have permission to delete this comment."
                }
            }
        ),
        404: openapi.Response(
            description="Comment not found.",
            examples={
                "application/json": {
                    "detail": "Comment not found."
                }
            }
        ),
    },
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    try:
        comment = BaseuserComment.objects.get(id=comment_id)
    except BaseuserComment.DoesNotExist:
        return Response(
            {_("detail"): _("Comment not found.")}, status=status.HTTP_404_NOT_FOUND
        )

    if comment.username != request.user:
        return Response(
            {_("detail"): _("You do not have permission to delete this comment.")},
            status=status.HTTP_403_FORBIDDEN,
        )

    comment.delete()

    return Response(
        {_("detail"): _("Comment deleted successfully.")}, status=status.HTTP_200_OK
    )

@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "comment": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="The comment text",
                example="i'm a nigga"
            )
        },
        required=["comment"],
    ),
    responses={
        201: openapi.Response(description="Comment added successfully."),
        403: openapi.Response(description="Cannot add comments to basic user profiles."),
        404: openapi.Response(description="Baseuser profile not found."),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_comment(request, username):
    try:
        baseuser_profile = BaseProfile.objects.get(base_user__username=username)
    except BaseProfile.DoesNotExist:
        return Response(
            {_("detail"): _("Baseuser profile not found.")}, status=status.HTTP_404_NOT_FOUND
        )
    if baseuser_profile.base_user.user_type == "basic":
        return Response(
            {_("detail"): _("Cannot add comments to basic user profiles.")},
            status=status.HTTP_403_FORBIDDEN,
        )

    user = request.user
    comment = request.data.get("comment")

    persianswear = PersianSwear()
    if not comment:
        return Response(
            {_("detail"): _("Comment is required.")}, status=status.HTTP_400_BAD_REQUEST
        )
    if persianswear.has_swear(comment):
        return Response(
            {_("detail"): _("Comment contains inappropriate language.")},
            status=status.HTTP_400_BAD_REQUEST,
        )

    new_comment = BaseuserComment.objects.create(
        baseuser_profile=baseuser_profile,
        username=user,
        comment=comment,
        time=timezone.now(),
    )

    serializer = BaseuserCommentSerializer(new_comment)
    return Response(
        {
            _("detail"): _("Comment added successfully."),
            "comment": {"id": new_comment.id, **serializer.data},
        },
        status=status.HTTP_201_CREATED,
    )


from authenticator.PersianSwear import PersianSwear
@swagger_auto_schema(
    method="put",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "comment": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="The updated comment text",
                example="i'm a nigga"
            )
        },
        required=["comment"],
    ),
    responses={
        200: openapi.Response(description="Comment updated successfully."),
        403: openapi.Response(description="You do not have permission to edit this comment."),
        404: openapi.Response(description="Comment not found."),
    },
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_comment(request, comment_id):
    try:
        comment = BaseuserComment.objects.get(id=comment_id)
    except BaseuserComment.DoesNotExist:
        return Response(
            {_("detail"): _("Comment not found.")}, status=status.HTTP_404_NOT_FOUND
        )

    if comment.username != request.user:
        return Response(
            {_("detail"): _("You do not have permission to edit this comment.")},
            status=status.HTTP_403_FORBIDDEN,
        )

    updated_comment = request.data.get("comment")
    if not updated_comment:
        return Response(
            {_("detail"): _("New comment text is required.")},
            status=status.HTTP_400_BAD_REQUEST,
        )

    persianswear = PersianSwear()
    if persianswear.has_swear(updated_comment):
        return Response(
            {_("detail"): _("Comment contains inappropriate language.")},
            status=status.HTTP_400_BAD_REQUEST,
        )

    comment.comment = updated_comment
    comment.save()

    return Response(
        {_("detail"): _("Comment updated successfully.")}, status=status.HTTP_200_OK
    )
