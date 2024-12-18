from django.contrib import admin
from .models import Position

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "position_user",  
        "name",
        "total",
        "funded",
        "is_done",
        "start_time",
        "end_time",
        "get_position_user_name",  
    ]
    list_editable = ["funded", "is_done"]
    search_fields = ["name", "position_user__username"]  
    list_filter = ["is_done", "start_time", "end_time"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("position_user")  

    def get_position_user_name(self, obj):
        return obj.position_user.username  

    get_position_user_name.short_description = "Position User"  
