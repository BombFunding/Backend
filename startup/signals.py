from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from team.models import Team
from startup.models import StartupProfile

@receiver(post_delete, sender=StartupProfile)
def delete_team_for_startup(sender, instance, **kwargs):
    try:
        team = Team.objects.get(startup_profile=instance)
        team.delete()
    except Team.DoesNotExist:
        pass        