from rest_framework import serializers
from .models import StartupComment
from authenticator.models import BaseUser  
from .models import StartupProfile
from rest_framework import serializers
from .models import StartupProfile
from rest_framework import serializers
from .models import StartupComment
from .models import StartupPosition

class StartupProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupProfile
        fields = ['startup_user', 'name', 'description', 'page', 'categories']


class StartupPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupPosition
        fields = ['name', 'description', 'total', 'funded', 'is_done', 'start_time', 'end_time']


class StartupCommentSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source='username.username')
    
    
    startup_profile = serializers.CharField(source='startup_profile.name')

    class Meta:
        model = StartupComment
        fields = ['id', 'startup_profile', 'username', 'comment', 'time']
