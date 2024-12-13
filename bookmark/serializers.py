from rest_framework import serializers
from django.db import IntegrityError
from .models import BookmarkUser
from authenticator.models import BaseUser

class BookmarkSerializer(serializers.ModelSerializer):
    target = serializers.CharField(write_only=True)
    target_username = serializers.CharField(source="target.username", read_only=True)

    class Meta:
        model = BookmarkUser
        fields = ["id", "target", "target_username"]

    def create(self, validated_data):
        request = self.context.get("request")
        owner = request.user
        target_username = validated_data.pop("target")
        try:
            target = BaseUser.objects.get(username=target_username)
        except BaseUser.DoesNotExist:
            raise serializers.ValidationError({"error": "User does not exist."})

        if owner == target:
            raise serializers.ValidationError({"error": "You cannot bookmark yourself."})

        try:
            bookmark = BookmarkUser.objects.create(owner=owner, target=target)
        except IntegrityError:
            raise serializers.ValidationError({"error": "Bookmark already exists."})
        return bookmark

    