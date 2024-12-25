from rest_framework import serializers
from .models import Project, ProjectImage, CATEGORIES

class ProjectSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'user', 'username', 'page', 'name', 'image', 'subcategories', 'description', 'creation_date']
        read_only_fields = ['user', 'id', 'username']

    def validate(self, attrs):
        if 'subcategories' in attrs:
            all_subcategories = [subcategory for category in CATEGORIES.values() for subcategory in category]
            if not all(subcategory in all_subcategories for subcategory in attrs['subcategories']):
                raise serializers.ValidationError("Invalid subcategory")
        return super().validate(attrs)

class ProjectImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectImage
        fields = ['id', 'user', 'image', 'created_at']
        read_only_fields = ['user', 'id', 'created_at']

class DashboardProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'image']