from django.db.models.signals import post_save
from django.dispatch import receiver
from startup.models import StartupProfile
from team.models import Team

@receiver(post_save, sender=StartupProfile)
def create_team_for_startup(sender, instance, created, **kwargs):
    if created:
        Team.objects.create(startup_profile=instance)