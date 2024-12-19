
from rest_framework import serializers
from .models import InvestorProfile

class InvestorProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestorProfile
        fields = [
        "investor_user",  
            "score",
            "investor_starting_date",
            "investor_profile_visit_count",
            "national_id",
            "legal_code",
            "iban",
            "tax_identification_number",
            "address"
        ]
