from django.db.models.signals import post_save
from django.dispatch import receiver
from startup.models import StartupUser
from team.models import Team

@receiver(post_save, sender=StartupUser)
def create_team_for_startup(sender, instance, created, **kwargs):
    if created:
        Team.objects.create(startup_user=instance)