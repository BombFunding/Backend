from django import forms
from django.contrib import admin

from .models import StartupApplication, StartupPosition

@admin.register(StartupPosition)
class StartupPositionAdmin(admin.ModelAdmin):
    list_display = [
        "startup_profile",
        "name",
        "total",
        "funded",
        "is_done",
        "start_time",
        "end_time",
        "get_startup_profile_name",
    ]
    list_editable = ["funded", "is_done"]
    search_fields = ["name", "startup_profile__name"]
    list_filter = ["is_done", "start_time", "end_time"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("startup_profile")

    def get_startup_profile_name(self, obj):
        return obj.startup_profile.name

    get_startup_profile_name.short_bio = "Startup Profile"


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

    get_startup_applicant_name.short_bio = "Startup Applicant"

    def get_investor_position_name(self, obj):
        return obj.investor_position.name if obj.investor_position else "-"

    get_investor_position_name.short_bio = "Investor Position"

