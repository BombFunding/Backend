from rest_framework import serializers
from .models import Transaction
from project.serializers import ProjectSerializer
from project.models import Project

class TransactionSerializer(serializers.ModelSerializer):
    position_description = serializers.CharField(source="position.description", read_only=True)
    project = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'investor_user', 'position', 'position_description', 'investment_amount', 'investment_date', 'project']

    def get_project_data(self, obj):
        return ProjectSerializer(Project.objects.get(positions=obj.position)).data
        

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['investment_amount', 'investment_date', 'position']

class ProjectInvestmentHistorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='investor_user.username')
    user_picture = serializers.ImageField(source='investor_user.profile.profile_picture', read_only=True)

    class Meta:
        model = Transaction
        fields = ['investment_amount', 'investment_date', 'username', 'user_picture']
