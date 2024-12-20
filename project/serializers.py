from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'user', 'username', 'page', 'name', 'image', 'category', 'description']
        read_only_fields = ['user', 'id', 'username']