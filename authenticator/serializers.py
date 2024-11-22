from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import BaseUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    required_fields = ['username', 'email', 'password', 'user_type']

    class Meta:
        model = BaseUser
        fields = ('id', 'username', 'email', 'user_type', 'password')

    def create(self, validated_data):
        for field in self.required_fields:
            if field not in validated_data:
                raise serializers.ValidationError({field: f"{field.capitalize()} is required."})
        user = BaseUser.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
                              
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False)

    def validate(self, data):
        if 'username' not in data and 'email' not in data:
            raise serializers.ValidationError("Username or email is required.")

        if 'username' in data:
            user = authenticate(username=data['username'], password=data['password'])

        if 'email' in data:
            try:
                user = BaseUser.objects.get(email=data['email'])
                user = authenticate(username=user.username, password=data['password'])
            except BaseUser.DoesNotExist:
                raise serializers.ValidationError("Invalid username or password.")


        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid username or password.")
