from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    position_description = serializers.CharField(source="position.description", read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'investor_user', 'position', 'position_description', 'investment_amount', 'investment_date']

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['investment_amount', 'investment_date', 'position']

class ProjectInvestmentHistorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='investor_user.username')

    class Meta:
        model = Transaction
        fields = ['investment_amount', 'investment_date', 'username']
