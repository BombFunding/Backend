from rest_framework import serializers

from .models import StartupPosition, BaseProfile



class StartupPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupPosition
        fields = ["name", "bio", "total", "funded", "is_done", "start_time", "end_time"]


