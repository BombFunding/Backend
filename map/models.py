
from django.db import models
from authenticator.models import BaseUser

class Pin(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='pins')

    def __str__(self):
        return f"Pin at ({self.latitude}, {self.longitude}) by {self.user.username}"
