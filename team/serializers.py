from rest_framework import serializers
from .models import TeamMember
from authenticator.models import BaseUser
from .mixins import UserFromUsernameMixin, TeamMixin

class TeamMemberSerializer(serializers.ModelSerializer, UserFromUsernameMixin, TeamMixin):
    username = serializers.CharField(write_only=True)
    role = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = TeamMember
        fields = ["username", "role", "description"]

    def validate(self, data):
        username = data.get("username")
        user = self.get_user(username)
        data["team"] = self.context["team"]

        if not user:
            raise serializers.ValidationError({"error": "User does not exist"})

        data["user"] = user
        
        return data

    def create(self, validated_data):
        validated_data.pop("username")

        if self.get_team_member(validated_data["user"], validated_data["team"]):
            raise serializers.ValidationError({"error": "User already in team"})

        team_member = TeamMember.objects.create(**validated_data)
        return team_member

    def update(self, instance, validated_data):
        instance.role = validated_data.get("role", instance.role)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance


class TeamMemberUpdateSerializer(serializers.ModelSerializer):
    role = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = TeamMember
        fields = ["role", "description"]

class TeamMemberListSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(source="user.baseprofile.profile_picture")
    username = serializers.CharField(source="user.username")

    class Meta:
        model = TeamMember
        fields = ["user", "username", "role", "description", "profile_pic"]