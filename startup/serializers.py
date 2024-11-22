from rest_framework import serializers
from .models import StartupComment
from authenticator.models import BaseUser  
from .models import StartupProfile
from rest_framework import serializers
from .models import StartupProfile
from rest_framework import serializers
from .models import StartupComment
from .models import StartupPosition

from rest_framework import serializers
from .models import StartupProfile

class StartupProfileSerializer(serializers.ModelSerializer):
    startup_user_username = serializers.CharField(source='startup_user.username.username', read_only=True)
    email = serializers.EmailField(source='startup_user.email', read_only=True)  
    about_me = serializers.CharField(required=False, allow_blank=True)
    socials = serializers.JSONField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = StartupProfile
        fields = [
            'id', 'startup_user_username', 'email', 'name', 'bio', 'page', 
            'categories', 'about_me', 'socials', 'phone', 'first_name', 'last_name'
        ]
        def update(self, instance, validated_data):
            startup_user_data = validated_data.get('startup_user', {})
            if isinstance(startup_user_data, dict):  
                for attr, value in startup_user_data.items():
                    setattr(instance, attr, value)
            return instance


class StartupPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupPosition
        fields = ['name', 'bio', 'total', 'funded', 'is_done', 'start_time', 'end_time']

        
class StartupCommentSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source='username.username')
    
    
    startup_profile = serializers.CharField(source='startup_profile.name')

    class Meta:
        model = StartupComment
        fields = ['id', 'startup_profile', 'username', 'comment', 'time']
