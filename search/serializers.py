from rest_framework import serializers
from authenticator.models import BaseUser

class BaseUserSerializer(serializers.ModelSerializer):
    startup_category = serializers.CharField(source="startupuser.startupprofile.startup_categories", read_only=True)

    class Meta:
        model = BaseUser
        fields = ["id", "username", "user_type", "startup_category"]
        