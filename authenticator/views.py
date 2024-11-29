from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django_email_verification import send_email
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import BaseUser,BaseProfile
from .serializers import (
    EmailSerializer,
    LoginSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
    BaseProfileSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_email(user)


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

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


class ForgetPasswordEmailView(generics.CreateAPIView):
    serializer_class = EmailSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f"http://localhost:3000/reset-password/{uid}/{token}"

        send_mail(
            subject="Reset your password",
            message=f"Click the link to reset your password: {reset_url}",
            from_email="sendemailviapython3@gmail.com",
            recipient_list=[user.email],
        )

        return Response({"message": "Email sent"}, status=status.HTTP_200_OK)


class ResetPasswordView(generics.CreateAPIView):
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
                {"message": e.message_dict}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Password reset successfully"}, status=status.HTTP_200_OK
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_user_password(request):
    user = request.user
    new_password = request.data.get("new_password")

    if not new_password:
        return Response(
            {"detail": "New password is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    password_field = BaseUser._meta.get_field("password")

    try:
        for validator in password_field.validators:
            validator(new_password)
    except DjangoValidationError as e:
        raise RestValidationError({"password": e.messages})

    user.set_password(new_password)
    user.save()

    return Response(
        {"detail": "Password updated successfully."}, status=status.HTTP_200_OK
    )

#######################################

@api_view(["GET"])
def baseuser_search_by_name(request, username):
    try:
        base_user = BaseUser.objects.get(username=username)
        startup_profile = BaseProfile.objects.get(base_user=base_user)

        return Response(
            {
                "startup_profile": {
                    "name": startup_profile.name,
                    "bio": startup_profile.bio,
                    "email": base_user.email, 
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
            },
            status=status.HTTP_200_OK,
        )

    except BaseUser.DoesNotExist:
        return Response(
            {"detail": "Startup user not found."}, status=status.HTTP_404_NOT_FOUND
        )
    except BaseProfile.DoesNotExist:
        return Response(
            {"detail": "Startup profile not found."}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view_own_baseuser_profile(request):
    user = request.user
    try:
        base_user = BaseUser.objects.get(username=user)
        base_profile = BaseProfile.objects.get(base_user=base_user)

        return Response(
            {
                "base_profile": {
                    "name": base_profile.name,
                    "bio": base_profile.bio,
                    "email": user.email,
                    "socials": base_profile.socials,
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
            {"detail": "Base user not found."}, status=status.HTTP_404_NOT_FOUND
        )
    except BaseProfile.DoesNotExist:
        return Response(
            {"detail": "Base profile not found."}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_baseuser_profile(request):
    user = request.user

    if user.user_type != "startup":
        return Response(
            {
                "detail": "Only users with 'startup' type can create or update a profile."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        base_user = BaseUser.objects.get(username=user)
    except BaseUser.DoesNotExist:
        return Response(
            {"detail": "No related base user found."}, status=status.HTTP_404_NOT_FOUND
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
        message = "Profile updated successfully."
    else:
        serializer = BaseProfileSerializer(data=request.data)
        message = "Profile created successfully."

    if serializer.is_valid():
        serializer.save(base_user=base_user)
        return Response(
            {
                "detail": message,
                "profile": {
                    "username": user.username,
                    "email": user.email,
                    **serializer.data,
                    "profile_picture": (
                        base_profile.profile_picture.url
                        if base_profile and base_profile.profile_picture
                        else None
                    ),
                    "header_picture": (
                        base_profile.header_picture.url
                        if base_profile and base_profile.header_picture
                        else None
                    ),
                },
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
