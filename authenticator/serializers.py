from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import BaseUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = BaseUser
        fields = ('id', 'username', 'email', 'name', 'about_me', 'user_type', 'password')

    def create(self, validated_data):
        if "user_type" not in validated_data:
            raise serializers.ValidationError({"user_type": "This field is required."})
        user = BaseUser.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
                              
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid username or password.")
