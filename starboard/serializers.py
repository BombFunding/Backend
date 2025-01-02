from profile_statics.models import ProjectStatistics
from project.models import Project
from rest_framework import serializers
from like.models import Like
from bookmark.models import Bookmark

class ProjectListSerializer(serializers.ModelSerializer):
    visit_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'image', 'description', 
                 'subcategories', 'visit_count', 'like_count', 'is_liked', 'is_bookmarked', 'creation_date']

    def get_visit_count(self, obj):
        try:
            return obj.statistics.get_total_visits()
        except ProjectStatistics.DoesNotExist:
            return 0

    def get_like_count(self, obj):
        try:
            return sum(len(likes) for likes in obj.statistics.likes.values())
        except ProjectStatistics.DoesNotExist:
            return 0
    
    def get_is_liked(self, obj):
        try:
            return Like.objects.filter(user=self.context['request'].user, project=obj).exists()
        except Exception:
            return None

    def get_is_bookmarked(self, obj):
        try:
            return Bookmark.objects.filter(owner=self.context['request'].user, target=obj).exists()
        except Exception:
            return None