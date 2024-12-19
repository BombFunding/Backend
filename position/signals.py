

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, BaseUser, Position

@receiver(post_save, sender=BaseUser)
def create_transaction(sender, instance, created, **kwargs):
    
    if not created:
        
        last_transaction = Transaction.objects.filter(investor_user=instance).last()
        if last_transaction:
            
            pass
