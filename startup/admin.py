from django import forms
from django.contrib import admin

from .models import Position, StartupProfile

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

