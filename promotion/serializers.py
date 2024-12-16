from rest_framework import serializers

class PromotionSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)