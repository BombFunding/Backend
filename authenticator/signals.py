from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from authenticator.models import BaseUser, BaseProfile, BasicUser, InvestorUser, StartupUser
from startup.models import StartupProfile
from django.db import transaction
from team.models import Team
from django.db.models.signals import post_save
from django.dispatch import receiver
from authenticator.models import BaseUser, BasicUser, InvestorUser, StartupUser
from startup.models import StartupProfile
from profile_statics.models import ProfileStatics  
from django.db import transaction


@receiver(post_save, sender=BaseUser)
def create_user_profile(sender, instance, created, **kwargs):
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
                startup_categories="Technology",
                startup_starting_date=None,
                startup_ending_date=None,
                startup_profile_visit_count=0,
            )

            
            ProfileStatics.objects.create(
                user=instance,  
                likes={},  
                views={},  
            )

        elif instance.user_type == "investor":
            
            InvestorUser.objects.create(username=instance)

            
            ProfileStatics.objects.create(
                user=instance,  
                likes={},  
                views={},  
            )

        elif instance.user_type == "basic":
            
            BasicUser.objects.create(username=instance)
