from django.contrib import admin
from .models import Project, ProjectImage

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'creation_date')
    list_filter = ('creation_date',)
    search_fields = ('name', 'user__username', 'description')
    readonly_fields = ('creation_date',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'description', 'image')
        }),
        ('Project Details', {
            'fields': ('page', 'subcategories')
        }),
        ('Metadata', {
            'fields': ('creation_date',),
            'classes': ('collapse',)
        })
    )

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'image_preview')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

    def image_preview(self, obj):
        return f'<img src="{obj.image.url}" width="50" height="50" />'
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'
