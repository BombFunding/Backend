from rest_framework import serializers
from .models import StartupProfile, StartupPosition

class StartupPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupPosition
        fields = ['id', 'name', 'bio', 'total', 'funded', 'is_done', 'start_time', 'end_time']

class StartupProfileSerializer(serializers.ModelSerializer):
    positions = StartupPositionSerializer(many=True, read_only=True)

    class Meta:
        model = StartupProfile
        fields = ['id', 'startup_user', 'startup_rank', 'startup_categories', 'startup_starting_date', 'startup_ending_date',
                  'startup_profile_visit_count', 'positions']
