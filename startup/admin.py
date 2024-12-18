from django import forms
from django.contrib import admin

from .models import StartupApplication, Position, StartupProfile

from django.contrib import admin
from .models import Position



@admin.register(StartupProfile)
class StartupProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "startup_user",
        "score",
        "startup_categories",
        "startup_starting_date",
        "startup_profile_visit_count",
    ]
    search_fields = ["startup_categories"]
    list_filter = ["startup_categories", "startup_starting_date"]


@admin.register(StartupApplication)
class StartupApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "startup_applicant",
        "investor_position",
        "get_startup_applicant_name",
        "get_investor_position_name",
    ]
    search_fields = ["startup_applicant__name", "investor_position__name"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("startup_applicant", "investor_position")

    def get_startup_applicant_name(self, obj):
        return obj.startup_applicant.name

    get_startup_applicant_name.short_description = "Startup Applicant"

    def get_investor_position_name(self, obj):
        return obj.investor_position.name if obj.investor_position else "-"

    get_investor_position_name.short_description = "Investor Position"
