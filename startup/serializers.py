from rest_framework import serializers
from .models import StartupProfile, StartupPosition, StartupVote
from rest_framework import serializers
from datetime import datetime

class StartupPositionSerializer(serializers.ModelSerializer):
    percent_funded = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = StartupPosition
        fields = [
            "id",
            "name",
            "description",
            "total",
            "funded",
            "is_done",
            "start_time",
            "end_time",
            "percent_funded",  
            "days_remaining",   
        ]

    def get_percent_funded(self, obj):
        if obj.total > 0:
            return (obj.funded / obj.total) * 100
        return 0  

    def get_days_remaining(self, obj):
        today = datetime.today().date()
        if obj.end_time and obj.end_time > today:
            remaining_days = (obj.end_time - today).days
            return remaining_days
        return 0  

class StartupProfileSerializer(serializers.ModelSerializer):
    positions = StartupPositionSerializer(many=True, read_only=True)

    class Meta:
        model = StartupProfile
        fields = [
            "id",
            "startup_user",
            "startup_categories",
            "startup_starting_date",
            "startup_profile_visit_count",
            "positions",
        ]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupVote
        fields = ["vote"]
