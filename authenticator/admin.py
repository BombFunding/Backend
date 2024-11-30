from django.contrib import admin
from django import forms
from .models import BaseUser, BasicUser, InvestorUser, StartupUser, BaseProfile, StartupProfile, BaseuserComment


class BaseUserAdminForm(forms.ModelForm):
    class Meta:
        model = BaseUser
        exclude = ["password"]  


class BaseUserAdmin(admin.ModelAdmin):
    form = BaseUserAdminForm
    list_display = (
        "username",
        "email",
        "user_type",
        "is_staff",
        "is_confirmed",
        "is_superuser",
    )
    search_fields = ("username", "email")
    list_filter = ("user_type", "is_staff", "is_superuser")


class BasicUserAdmin(admin.ModelAdmin):
    list_display = ("get_username",)
    search_fields = ("username__username",)

    def get_username(self, obj):
        return obj.username.username

    get_username.admin_order_field = "username"
    get_username.short_description = "Username"


class InvestorUserAdmin(admin.ModelAdmin):
    list_display = ("get_username",)
    search_fields = ("username__username",)

    def get_username(self, obj):
        return obj.username.username

    get_username.admin_order_field = "username"
    get_username.short_description = "Username"


class StartupUserAdmin(admin.ModelAdmin):
    list_display = ("get_username",)
    search_fields = ("username__username",)

    def get_username(self, obj):
        return obj.username.username

    get_username.admin_order_field = "username"
    get_username.short_description = "Username"


class BaseProfileAdmin(admin.ModelAdmin):
    list_display = ["get_startup_user_name", "email", "first_name", "last_name"]
    search_fields = ["name", "base_user__username", "email"]

    def get_startup_user_name(self, obj):
        return obj.name

    get_startup_user_name.short_description = "Base Name"


@admin.register(BaseuserComment)
class BaseuserCommentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "get_commenter_username",
        "get_baseuser_profile_name",
        "comment",
        "time",
    ]
    search_fields = ["username__username", "baseuser_profile__name", "comment"]
    list_filter = ["time"]
    actions = ["delete_selected"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("baseuser_profile", "username")

    def get_baseuser_profile_name(self, obj):
        return obj.baseuser_profile.name

    get_baseuser_profile_name.short_description = "Comment on Baseuser Profile"

    def get_commenter_username(self, obj):
        return obj.username.username

    get_commenter_username.short_description = "Commenter Username"


admin.site.register(BaseUser, BaseUserAdmin)
admin.site.register(BasicUser, BasicUserAdmin)
admin.site.register(InvestorUser, InvestorUserAdmin)
admin.site.register(StartupUser, StartupUserAdmin)
admin.site.register(BaseProfile, BaseProfileAdmin)