from rest_framework import serializers
from .models import StartupProfile, StartupVote
from rest_framework import serializers
from datetime import datetime, date 


class StartupProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StartupProfile
        fields = [
            "id",
            "startup_user",
            "startup_categories",
            "startup_starting_date",
            "startup_profile_visit_count",
        ]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupVote
        fields = ["vote"]
