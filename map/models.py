
from django.conf import settings
from django.db import models

class Pin(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  
        blank=True  
    )
