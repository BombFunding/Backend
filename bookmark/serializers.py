from rest_framework import serializers
from .models import Bookmark

class BookmarkStatusSerializer(serializers.Serializer):
    has_bookmarked = serializers.BooleanField()

class BookmarkedProjectSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(source='target.id')
    project_header_picture = serializers.CharField(source='target.image.url')
    project_name = serializers.CharField(source='target.name')

    class Meta:
        model = Bookmark
        fields = ['project_id', 'project_header_picture', 'project_name']

class BookmarkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = []  # Empty fields since we get project_id from URL
