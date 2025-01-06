from rest_framework import serializers
from .models import Project, ProjectImage, CATEGORIES
from position.serializers import PositionSerializer
from like.models import Like

class ProjectSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    position_ids = serializers.SerializerMethodField()
    positions = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'user', 'username', 'page', 'name', 'image', 'subcategories', 'description', 'creation_date', 'position_ids', 'positions', 'like_count']
        read_only_fields = ['user', 'id', 'username']

    def get_position_ids(self, obj):
        return [position.id for position in obj.positions.all()]

    def get_positions(self, obj):
        return PositionSerializer(obj.positions.all(), many=True).data
    
    def get_like_count(self, obj):
        return Like.objects.filter(project=obj).count()

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