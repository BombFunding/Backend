from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import BaseUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ('id', 'username', 'email', 'name', 'about_me', 'user_type')

    def create(self, validated_data):
        
        validated_data['username'] = validated_data['username'].strip().lower()
        return super().create(validated_data)
                              
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid username or password.")
