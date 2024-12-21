from django.contrib import admin
from .models import Position
from django.contrib.postgres.forms import SimpleArrayField
from django.db import models  
from django.contrib.postgres.fields import ArrayField  


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
        "subcategory",  
        "get_position_user_name",  
    ]
    list_editable = ["funded", "is_done", "subcategory"]  
    search_fields = ["name", "position_user__username", "subcategory"]  
    list_filter = ["is_done", "start_time", "end_time", "subcategory"]  
    
    formfield_overrides = {
        ArrayField: {'widget': SimpleArrayField}
    }

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("position_user")  

    def get_position_user_name(self, obj):
        return obj.position_user.username  

    get_position_user_name.short_description = "Position User"



from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'investor_user', 'position', 'investment_amount', 'investment_date')
    search_fields = ('investor_user__username', 'position__name')
    list_filter = ('investment_date',)
    ordering = ('-investment_date',)

admin.site.register(Transaction, TransactionAdmin)
