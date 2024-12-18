from django.contrib import admin
from .models import InvestorProfile

@admin.register(InvestorProfile)
class InvestorProfileAdmin(admin.ModelAdmin):
    list_display = ("investor_user", "score", "investor_starting_date", "national_id")
    fields = (        
            "score",
            "investor_starting_date",
            "investor_profile_visit_count",
            "national_id",
            "legal_code",
            "iban",
            "tax_identification_number",
            "address"
    )


