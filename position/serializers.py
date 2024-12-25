from rest_framework import serializers
from .models import Position, Transaction
from datetime import datetime, date 

class PositionSerializer(serializers.ModelSerializer):
    percent_funded = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()
    project_name = serializers.CharField(source="project.name", read_only=True)

    class Meta:
        model = Position
        fields = [
            "id",
            "project",
            "project_name",
            "description",
            "total",
            "funded",
            "is_done",
            "start_time",
            "end_time",
            "percent_funded",
            "days_remaining",
        ]
        extra_kwargs = {
            'start_time': {'required': True},
            # 'end_time': {'required': True},
            'total': {'required': True},
            # 'description': {'required': True},
        }

    def get_percent_funded(self, obj):
        if obj.total > 0:
            return (obj.funded / obj.total) * 100
        return 0  

    def get_days_remaining(self, obj):
        today = date.today()  
        if obj.end_time and obj.end_time.date() > today:  
            remaining_days = (obj.end_time.date() - today).days  
            return remaining_days
        return 0

class TransactionSerializer(serializers.ModelSerializer):
    position_description = serializers.CharField(source="position.description", read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'investor_user', 'position', 'position_description', 'amount', 'transaction_date']

class PositionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['start_time', 'end_time', 'is_closed', 'total', 'funded']

class PositionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['end_time', 'total', 'description', 'project', 'start_time']
        read_only_fields = ['project']

class PositionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['total', 'description']