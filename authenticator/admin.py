from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from .models import BaseUser, BasicUser, InvestorUser, StartupUser , BasicUserProfile
from django.contrib import admin
from .models import BasicUserProfile


class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff','is_confirmed', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('user_type', 'is_staff', 'is_superuser')



class BasicUserAdmin(admin.ModelAdmin):
    list_display = ('get_username',)
    search_fields = ('username__username',)

    def get_username(self, obj):
        return obj.username.username  
    get_username.admin_order_field = 'username'
    get_username.short_description = 'Username'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        basic_user = self.get_object(request, object_id)
        base_user_id = basic_user.username.id
        return redirect(reverse('admin:authenticator_baseuser_change', args=[base_user_id]))

class InvestorUserAdmin(admin.ModelAdmin):
    list_display = ('get_username',)
    search_fields = ('username__username',)

    def get_username(self, obj):
        return obj.username.username  
    get_username.admin_order_field = 'username'
    get_username.short_description = 'Username'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        investor_user = self.get_object(request, object_id)
        base_user_id = investor_user.username.id
        return redirect(reverse('admin:authenticator_baseuser_change', args=[base_user_id]))

class StartupUserAdmin(admin.ModelAdmin):
    list_display = ('get_username',)
    search_fields = ('username__username',)

    def get_username(self, obj):
        return obj.username.username  
    get_username.admin_order_field = 'username'
    get_username.short_description = 'Username'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        startup_user = self.get_object(request, object_id)
        base_user_id = startup_user.username.id
        return redirect(reverse('admin:authenticator_baseuser_change', args=[base_user_id]))


@admin.register(BasicUserProfile)
class BasicUserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'interests', 'profile_picture']

admin.site.register(BaseUser, BaseUserAdmin)
admin.site.register(BasicUser, BasicUserAdmin)
admin.site.register(InvestorUser, InvestorUserAdmin)
admin.site.register(StartupUser, StartupUserAdmin)
