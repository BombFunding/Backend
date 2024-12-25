from django.contrib import admin
from .models import Position, Transaction
from django.contrib.postgres.forms import SimpleArrayField
from django.contrib.postgres.fields import ArrayField  


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "project",  
        "description",
        "total",
        "funded",
        "start_time",
        "end_time",
        "get_project_name",  
    ]
    list_editable = ["funded"]  
    search_fields = ["description", "project__name"]  
    list_filter = ["start_time", "end_time"]  
    
    formfield_overrides = {
        ArrayField: {'widget': SimpleArrayField}
    }

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("project")  

    def get_project_name(self, obj):
        return obj.project.name  

    get_project_name.short_description = "Project"

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'investor_user', 'position', 'investment_amount', 'investment_date')
    search_fields = ('investor_user__username', 'position__description')
    list_filter = ('investment_date',)
    ordering = ('-investment_date',)