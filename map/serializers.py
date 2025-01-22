
from rest_framework import serializers
from map.models import Pin

class PinSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Pin
        fields = ['id', 'latitude', 'longitude', 'user', 'username', 'email']
        read_only_fields = ['user', 'username', 'email']
