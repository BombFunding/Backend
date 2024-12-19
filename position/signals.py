from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, BaseUser

@receiver(post_save, sender=BaseUser)
def create_transaction(sender, instance, created, **kwargs):
    """
    Signal that triggers after a BaseUser instance is saved.
    It works for both Admin and API save actions.
    """
    if not created:
        
        last_transaction = Transaction.objects.filter(investor_user=instance).last()
        if last_transaction:
            
            pass
