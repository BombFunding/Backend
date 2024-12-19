from django.contrib import admin
from .models import ProfileStatics
from django.utils.safestring import mark_safe
import json

@admin.register(ProfileStatics)
class ProfileStaticsAdmin(admin.ModelAdmin):
    list_display = ("user", "display_likes", "display_views")  
    search_fields = ("user__username", "user__email")  
    list_filter = ("user__user_type",)  
    readonly_fields = ("user", "display_likes", "display_views")  

    def display_likes(self, obj):
        likes_data = json.dumps(obj.likes, indent=2)  
        return mark_safe(f"<pre>{likes_data}</pre>")  

    def display_views(self, obj):
        views_data = json.dumps(obj.views, indent=2)
        return mark_safe(f"<pre>{views_data}</pre>")

    display_likes.short_description = "Likes (JSON Format)"
    display_views.short_description = "Views (JSON Format)"
