from django.contrib import admin
from .models import Transaction

# Register your models here.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'investor_user', 'position', 'investment_amount', 'investment_date')
    search_fields = ('investor_user__username', 'position__description')
    list_filter = ('investment_date',)
    ordering = ('-investment_date',)