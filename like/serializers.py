from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'project', 'created_at']
        read_only_fields = ['user', 'created_at', 'project']

class LikeCountSerializer(serializers.Serializer):
    likes = serializers.IntegerField()

class HasLikedSerializer(serializers.Serializer):
    has_liked = serializers.BooleanField()
