from rest_framework import serializers
from .models import LikedSubcategories
from project.models import CATEGORIES

def get_all_subcategories():
    return [subcategory for category in CATEGORIES.values() for subcategory in category]

class LikedSubcategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedSubcategories
        fields = ['subcategories']

    def validate_subcategories(self, value):
        all_subcategories = get_all_subcategories()
        if not all(subcategory in all_subcategories for subcategory in value):
            raise serializers.ValidationError("Invalid subcategory")
        return value

class CategoryOperationSerializer(serializers.Serializer):
    subcategory = serializers.CharField(required=True)

    def validate_subcategory(self, value):
        all_subcategories = get_all_subcategories()
        if value not in all_subcategories:
            raise serializers.ValidationError(
                f"Category '{value}' is not a valid subcategory. Must be one of {all_subcategories}"
            )
        return value
