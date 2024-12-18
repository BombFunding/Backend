from django import forms
from django.contrib import admin

from .models import StartupApplication, Position, StartupProfile

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
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
    search_fields = ["name", "startup_profile__base_profile__name"]
    list_filter = ["is_done", "start_time", "end_time"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("startup_profile")

    def get_startup_profile_name(self, obj):
        return obj.startup_profile.startup_user.username

    get_startup_profile_name.short_description = "Startup Profile"

@admin.register(StartupProfile)
class StartupProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "startup_user",
        "score",
        "startup_categories",
        "startup_starting_date",
        "startup_profile_visit_count",
        "get_positions_count",
        "get_position_ids",
    ]
    search_fields = ["startup_categories"]
    list_filter = ["startup_categories", "startup_starting_date"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("Position_set")

    def get_positions_count(self, obj):
        return obj.Position_set.count()

    get_positions_count.short_description = "Number of Positions"

    def get_position_ids(self, obj):
        position_ids = [position.id for position in obj.Position_set.all()]
        return ", ".join(map(str, position_ids))

    get_position_ids.short_description = "Position IDs"

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
