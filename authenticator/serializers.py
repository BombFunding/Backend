from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import BaseUser
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    required_fields = ["username", "email", "password", "user_type"]

    class Meta:
        model = BaseUser
        fields = (
            "id",
            "username",
            "email",
            "name",
            "about_me",
            "user_type",
            "password",
        )

    def create(self, validated_data):
        for field in self.required_fields:
            if field not in validated_data:
                raise serializers.ValidationError(
                    {field: f"{field.capitalize()} is required."}
                )
        user = BaseUser.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


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
                return {
                    "user": user,
                    "password": data["password"]
                }
        except (TypeError, ValueError, OverflowError, BaseUser.DoesNotExist):
            pass

        raise serializers.ValidationError("Invalid reset link.")