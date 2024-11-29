from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import BaseUser


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
            raise serializers.ValidationError({str(_("error")): _("Username or email is required.")})

        if "username" in data:
            user = authenticate(username=data["username"], password=data["password"])

        if "email" in data:
            try:
                user = BaseUser.objects.get(email=data["email"])
                user = authenticate(username=user.username, password=data["password"])
            except BaseUser.DoesNotExist:
                raise serializers.ValidationError({str(_("error")): _("Invalid username or password.")})

        if user and user.is_confirmed and user.is_active:
            return user
        elif user and not user.is_confirmed:
            raise serializers.ValidationError({str(str(_("error"))): _("Email is not confirmed.")})

        raise serializers.ValidationError({str(_("error")): _("Invalid username or password.")})


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        try:
            user = BaseUser.objects.get(email=(data["email"]))
            return user
        except BaseUser.DoesNotExist:
            raise serializers.ValidationError({str(_("error")): _("Email does not exist.")})


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

        raise serializers.ValidationError({str(_("error")): _("Invalid reset link.")})
