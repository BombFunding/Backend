from rest_framework import serializers
from .models import StartupProfile
from .models import StartupPosition

class StartupProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupProfile
        fields = ['startup_user', 'name', 'description', 'page', 'categories']


class StartupPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupPosition
        fields = ['name', 'description', 'total', 'funded', 'is_done', 'start_time', 'end_time']
