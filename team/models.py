from django.db import models

from startup.models import StartupUser
from authenticator.models import BaseUser

class Team(models.Model):
    startup_user = models.OneToOneField(StartupUser, on_delete=models.CASCADE, default=None)

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)