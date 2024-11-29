from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .models import BaseUser, BasicUser, InvestorUser, StartupUser
from django import forms
from django.contrib import admin
from .models import BaseProfile



class BaseUserAdmin(admin.ModelAdmin):
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

    def change_view(self, request, object_id, form_url="", extra_context=None):
        basic_user = self.get_object(request, object_id)
        base_user_id = basic_user.username.id
        return redirect(
            reverse("admin:authenticator_baseuser_change", args=[base_user_id])
        )


class InvestorUserAdmin(admin.ModelAdmin):
    list_display = ("get_username",)
    search_fields = ("username__username",)

    def get_username(self, obj):
        return obj.username.username

    get_username.admin_order_field = "username"
    get_username.short_description = "Username"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        investor_user = self.get_object(request, object_id)
        base_user_id = investor_user.username.id
        return redirect(
            reverse("admin:authenticator_baseuser_change", args=[base_user_id])
        )


class StartupUserAdmin(admin.ModelAdmin):
    list_display = ("get_username",)
    search_fields = ("username__username",)

    def get_username(self, obj):
        return obj.username.username

    get_username.admin_order_field = "username"
    get_username.short_description = "Username"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        startup_user = self.get_object(request, object_id)
        base_user_id = startup_user.username.id
        return redirect(
            reverse("admin:authenticator_baseuser_change", args=[base_user_id])
        )


class BaseProfileForm(forms.ModelForm):
    class Meta:
        model = BaseProfile
        fields = "__all__"

    bio = forms.CharField(required=False, widget=forms.Textarea, initial="")
    phone = forms.CharField(required=False, initial="")
    socials = forms.JSONField(required=False, initial={})
    first_name = forms.CharField(required=False, initial="")
    last_name = forms.CharField(required=False, initial="")


@admin.register(BaseProfile)
class BaseProfileAdmin(admin.ModelAdmin):
    list_display = ["get_startup_user_name", "email", "first_name", "last_name"]
    search_fields = ["name", "base_user__username", "email"]
    form = BaseProfileForm

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("base_user")

    def get_startup_user_name(self, obj):
        return obj.name

    get_startup_user_name.short_description = "base Name"


admin.site.register(BaseUser, BaseUserAdmin)
admin.site.register(BasicUser, BasicUserAdmin)
admin.site.register(InvestorUser, InvestorUserAdmin)
admin.site.register(StartupUser, StartupUserAdmin)
