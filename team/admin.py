from django.contrib import admin

from .models import Team, TeamMember


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("startup_user",)
    search_fields = ("startup_user",)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("team", "user", "role", "description")
    search_fields = ("user__username",)