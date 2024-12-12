from rest_framework import serializers
from .models import StartupProfile, StartupPosition, StartupVote


class StartupPositionSerializer(serializers.ModelSerializer):
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
        ]

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
