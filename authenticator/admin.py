from django.contrib import admin
from .models import BaseUser, BasicUser, InvestorUser, StartupUser

class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'user_type', 'is_confirmed', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('user_type', 'is_confirmed', 'is_staff', 'is_superuser')

class BasicUserAdmin(admin.ModelAdmin):
    list_display = ('get_username',)
    search_fields = ('username__username',)  

    def get_username(self, obj):
        return obj.username.username  
    get_username.admin_order_field = 'username'  
    get_username.short_description = 'Username'  

class InvestorUserAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'page', 'categories')
    search_fields = ('username__username',)  
    list_filter = ('username__user_type',)

    def get_username(self, obj):
        return obj.username.username  
    get_username.admin_order_field = 'username'  
    get_username.short_description = 'Username'  

class StartupUserAdmin(admin.ModelAdmin):
    list_display = ('get_username',)
    search_fields = ('username__username',)  

    def get_username(self, obj):
        return obj.username.username  
    get_username.admin_order_field = 'username'  
    get_username.short_description = 'Username'  


admin.site.register(BaseUser, BaseUserAdmin)
admin.site.register(BasicUser, BasicUserAdmin)
admin.site.register(InvestorUser, InvestorUserAdmin)
admin.site.register(StartupUser, StartupUserAdmin)
