from rest_framework import serializers
from .models import Investor

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = [
            "full_name",
            "email",
            "phone_number",
            "address",
            "national_id",
            "tax_identification_number",
            "investor_starting_date",
        ]
