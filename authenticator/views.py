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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import BaseUser, BasicUserProfile
from .serializers import (
    EmailSerializer,
    LoginSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_email(user)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_description="Login to the application and get tokens to authenticate future requests.",
        responses={200: openapi.Response("ورود موفقیت آمیز"), 400: "نام کاربری یا رمز عبور نامعتبر است."},
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
        responses={200: "ایمیل ارسال شد", 400: "ایمیل وجود ندارد."},
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
            subject="عوض کردن رمز عبور",
            message=f"روی لینک روبرو کلیک کنید تا رمز عبور خود را عوض کنید. {reset_url}",
            from_email="sendemailviapython3@gmail.com",
            recipient_list=[user.email],
        )

        return Response({"پیام": "ایمیلی به شما برای عوض کردن رمز عبورتون ارسال شد."}, status=status.HTTP_200_OK)


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
                {"message": e.message_dict}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"پیام": "رمز عبور با موفقیت عوض شد."}, status=status.HTTP_200_OK
        )


# TODO: Add serializers for the following views wherever necessary
class ViewOwnBasicUserProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="View the authenticated user's basic profile.",
        responses={200: "پروفایل با موفقیت بازیابی شد", 404: "پروفایل یافت نشد"},
        tags=["profile"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
        
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            basic_user_profile = BasicUserProfile.objects.get(username=user)

            profile_picture_url = None
            header_picture_url = None
            if (basic_user_profile.profile_picture):
                profile_picture_url = request.build_absolute_uri(
                    basic_user_profile.profile_picture.url
                )
            if (basic_user_profile.header_picture):
                header_picture_url = request.build_absolute_uri(
                    basic_user_profile.header_picture.url
                )

            return Response(
                {
                    "basic_user_profile": {
                        "username": user.username,
                        "email": user.email,
                        "interests": basic_user_profile.interests,
                        "profile_picture": profile_picture_url,
                        "header_picture": header_picture_url,
                    }
                },
                status=status.HTTP_200_OK,
            )

        except BasicUserProfile.DoesNotExist:
            return Response(
                {"خطا": "پروفایل کاربر پایه یافت نشد."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({"خطا": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ViewBasicUserProfileView(GenericAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="View a user's basic profile by username.",
        responses={200: "پروفایل با موفقیت بازیابی شد", 404: "پروفایل یافت نشد"},
        tags=["profile"],
    )
    def get(self, request, username, *args, **kwargs):
        try:
            basic_user_profile = BasicUserProfile.objects.get(username__username=username)
            user = basic_user_profile.username

            profile_picture_url = None
            header_picture_url = None
            if basic_user_profile.profile_picture:
                profile_picture_url = request.build_absolute_uri(
                    basic_user_profile.profile_picture.url
                )
            if basic_user_profile.header_picture:
                header_picture_url = request.build_absolute_uri(
                    basic_user_profile.header_picture.url
                )

            return Response(
                {
                    "basic_user_profile": {
                        "username": user.username,
                        "email": user.email,
                        "profile_picture": profile_picture_url,
                        "header_picture": header_picture_url,
                    }
                },
                status=status.HTTP_200_OK,
            )

        except BasicUserProfile.DoesNotExist:
            return Response(
                {"خطا": "پروفایل کاربر پایه یافت نشد."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({"خطا": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UpdateBasicUserProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update the authenticated user's basic profile.",
        responses={200: "پروفایل با موفقیت به روز شد", 400: "درخواست نامعتبر"},
        tags=["profile"],
    )
    def patch(self, request, *args, **kwargs):
        user = request.user
        try:
            basic_user_profile, created = BasicUserProfile.objects.get_or_create(
                username=user
            )

            data = request.data

            if "email" in data:
                user.email = data["email"]
            if "password" in data:
                user.set_password(data["password"])

            user.save()
            if "interests" in data:
                basic_user_profile.interests = data["interests"]
            if "profile_picture" in request.FILES:
                basic_user_profile.profile_picture = request.FILES["profile_picture"]
            if "header_picture" in request.FILES:
                basic_user_profile.header_picture = request.FILES["header_picture"]

            basic_user_profile.save()

            return Response(
                {"خطا": "پروفایل با موفقیت به روز شد."}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({"خطا": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangeUserPasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Change the authenticated user's password.",
        responses={200: "رمز عبور با موفقیت به روز شد", 400: "درخواست نامعتبر"},
        tags=["auth"],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        new_password = request.data.get("new_password")

        if not new_password:
            return Response(
                {"خطا": "رمز عبور جدید مورد نیاز است."}, status=status.HTTP_400_BAD_REQUEST
            )

        user.change_password(new_password)

        return Response(
            {"خطا": "رمز عبور با موفقیت به روز شد."}, status=status.HTTP_200_OK
        )
