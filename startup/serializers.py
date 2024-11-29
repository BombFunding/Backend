from rest_framework import serializers

from .models import StartupComment, StartupPosition, BaseProfile



class StartupPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupPosition
        fields = ["name", "bio", "total", "funded", "is_done", "start_time", "end_time"]


class StartupCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="username.username")

    startup_profile = serializers.CharField(source="startup_profile.name")

    class Meta:
        model = StartupComment
        fields = ["id", "startup_profile", "username", "comment", "time"]
