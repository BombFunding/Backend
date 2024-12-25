from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from authenticator.models import BaseUser, BaseProfile, BasicUser,  StartupUser
from startup.models import StartupProfile
from django.db import transaction
from team.models import Team
from django.db.models.signals import post_save
from django.dispatch import receiver
from authenticator.models import BaseUser, BasicUser, StartupUser
from startup.models import StartupProfile
from profile_statics.models import ProfileStatics  
from django.db import transaction
from django.utils import timezone


@receiver(post_save, sender=BaseUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates related profiles for users based on their user type 
    when a new BaseUser is created, regardless of whether it's via
    request or admin panel.
    """
    if created:
        
        base_profile = BaseProfile.objects.create(
            base_user=instance,
            name=instance.username,
            email=instance.email,
            bio="",
        )
        
        
        if instance.user_type == "startup":
            startup_user = StartupUser.objects.create(username=instance)
            StartupProfile.objects.create(
                startup_user=startup_user,
                startup_starting_date=timezone.now().date(),
                startup_profile_visit_count=0,
            )
            ProfileStatics.objects.create(
                user=instance,
                likes={},
                views={},
            )

        
        elif instance.user_type == "basic":
            BasicUser.objects.create(username=instance)