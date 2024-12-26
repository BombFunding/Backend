from rest_framework import serializers
from .models import Comment

class CommentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'project']
        read_only_fields = ['project']

class CommentOutputSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='author.profile.profile_picture', read_only=True)
    profile_id = serializers.IntegerField(source='author.profile.id', read_only=True)
    username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'updated_at', 'profile_id', 'username', 'profile_picture']