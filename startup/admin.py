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
        "startup_starting_date",
        "startup_profile_visit_count",
    ]
    list_filter = ["startup_starting_date","startup_ending_date"]

