from rest_framework import serializers
from authenticator.models import BaseUser
from startup.models import StartupUser
from project.models import Project

class BaseUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)

    class Meta:
        model = BaseUser
        fields = ["id", "username", "profile_picture"]

class StartupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='username.username')
    profile_picture = serializers.ImageField(source='username.profile.profile_picture', read_only=True)

    class Meta:
        model = StartupUser
        fields = ["id", "username", "profile_picture"]

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "image"]
