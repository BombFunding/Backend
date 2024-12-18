from django.db import models
from authenticator.models import BaseUser
from datetime import date

class Project(models.Model):
    user = models.OneToOneField(
        BaseUser,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type__in": ["startup", "investor"]},
        )
    peage_builder = models.JSONField(default=dict, blank=True)
