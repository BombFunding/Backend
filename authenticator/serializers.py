from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from .models import BaseUser, BaseProfile


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ["email", "username", "password", "user_type"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)

    def validate(self, data):
        if "username" not in data and "email" not in data:
            raise serializers.ValidationError("Username or email is required.")

        if "username" in data:
            user = authenticate(username=data["username"], password=data["password"])

        if "email" in data:
            try:
                user = BaseUser.objects.get(email=data["email"])
                user = authenticate(username=user.username, password=data["password"])
            except BaseUser.DoesNotExist:
                raise serializers.ValidationError("Invalid username or password.")

        if user and user.is_confirmed and user.is_active:
            return user
        elif user and not user.is_confirmed:
            raise serializers.ValidationError("Email is not confirmed.")

        raise serializers.ValidationError("Invalid username or password.")


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        try:
            user = BaseUser.objects.get(email=data["email"])
            return user
        except BaseUser.DoesNotExist:
            raise serializers.ValidationError("Email does not exist.")


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            decoded_uid = urlsafe_base64_decode(data["uid"])
            user = BaseUser.objects.get(pk=decoded_uid)
            token_generator = PasswordResetTokenGenerator()
            if token_generator.check_token(user, data["token"]):
                return {"user": user, "password": data["password"]}
        except (TypeError, ValueError, OverflowError, BaseUser.DoesNotExist):
            pass

        raise serializers.ValidationError("Invalid reset link.")


class BaseProfileSerializer(serializers.ModelSerializer):
    startup_user_username = serializers.CharField(
        source="startup_user.username.username", read_only=True
    )
    email = serializers.EmailField(source="startup_user.email", read_only=True)
    socials = serializers.JSONField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    header_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = BaseProfile
        fields = [
            "id",
            "startup_user_username",
            "email",
            "name",
            "bio",
            "socials",
            "phone",
            "first_name",
            "last_name",
            "profile_picture",
            "header_picture",
        ]

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.socials = validated_data.get("socials", instance.socials)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        if "profile_picture" in validated_data:
            instance.profile_picture = validated_data.get(
                "profile_picture", instance.profile_picture
            )
        if "header_picture" in validated_data:
            instance.header_picture = validated_data.get(
                "header_picture", instance.header_picture
            )

        instance.save()
        return instance
