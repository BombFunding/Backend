from django.contrib import admin
from .models import StartupProfile, StartupPosition, StartupComment, StartupApplication
from .models import BaseUser  # Ensure you import BaseUser

@admin.register(StartupProfile)
class StartupProfileAdmin(admin.ModelAdmin):
    list_display = ['startup_user', 'name', 'description', 'get_startup_user_name']
    search_fields = ['name', 'startup_user__username']
    list_filter = ['categories']
    readonly_fields = ['page', 'categories']

    def get_startup_user_name(self, obj):
        return obj.startup_user.username
    get_startup_user_name.short_description = 'Startup User'

@admin.register(StartupPosition)
class StartupPositionAdmin(admin.ModelAdmin):
    list_display = [
        'startup_profile', 'name', 'total', 'funded', 'is_done', 'start_time', 'end_time',
        'get_startup_profile_name'
    ]
    list_editable = ['funded', 'is_done']
    search_fields = ['name', 'startup_profile__name']
    list_filter = ['is_done', 'start_time', 'end_time']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('startup_profile')

    def get_startup_profile_name(self, obj):
        return obj.startup_profile.name
    get_startup_profile_name.short_description = 'Startup Profile'

@admin.register(StartupComment)
class StartupCommentAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'startup_profile', 'comment', 'time', 'get_startup_profile_name']
    search_fields = ['username__username', 'startup_profile__name', 'comment']
    list_filter = ['time']
    actions = ['delete_selected']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('startup_profile', 'username')

    def get_startup_profile_name(self, obj):
        return obj.startup_profile.name
    get_startup_profile_name.short_description = 'Startup Profile'

    def get_username(self, obj):
        return obj.username.username  # This ensures the username from BaseUser is displayed
    get_username.short_description = 'Commenter Username'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "username":
            # Show all BaseUser related users (instead of specific models like StartupUser or InvestorUser)
            kwargs["queryset"] = BaseUser.objects.all()  
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(StartupApplication)
class StartupApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'startup_applicant', 'investor_position',
        'get_startup_applicant_name', 'get_investor_position_name'
    ]
    search_fields = ['startup_applicant__name', 'investor_position__name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('startup_applicant', 'investor_position')

    def get_startup_applicant_name(self, obj):
        return obj.startup_applicant.name
    get_startup_applicant_name.short_description = 'Startup Applicant'

    def get_investor_position_name(self, obj):
        return obj.investor_position.name if obj.investor_position else "-"
    get_investor_position_name.short_description = 'Investor Position'
