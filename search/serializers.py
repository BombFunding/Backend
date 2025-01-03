from rest_framework import serializers
from authenticator.models import BaseUser
from startup.models import StartupUser
from project.models import Project
from profile_statics.models import ProjectStatistics

class BaseUserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)
    user_id = serializers.IntegerField(source='id', read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = BaseUser
        fields = ["user_id", "username", "name", "profile_picture"]

    def get_name(self, obj):
        return f"{obj.profile.first_name} {obj.profile.last_name}"

class StartupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='username.username')
    profile_picture = serializers.ImageField(source='username.profile.profile_picture', read_only=True)
    profile_id = serializers.IntegerField(source='startup_profile.id', read_only=True)
    user_id = serializers.IntegerField(source='username.id', read_only=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = StartupUser
        fields = ["profile_id", "user_id", "username", "name", "profile_picture"]

    def get_name(self, obj):
        return f"{obj.username.profile.first_name} {obj.username.profile.last_name}"

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "image"]

class ProjectListSerializer(serializers.ModelSerializer):
    visit_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'image', 'description', 
                 'subcategories', 'visit_count', 'like_count', 'creation_date']

    def get_visit_count(self, obj):
        try:
            return obj.statistics.get_total_visits()
        except ProjectStatistics.DoesNotExist:
            return 0

    def get_like_count(self, obj):
        try:
            return sum(len(likes) for likes in obj.statistics.likes.values())
        except ProjectStatistics.DoesNotExist:
            return 0
