from django.db import models
from startup.models import StartupProfile

class ProfilePageImage(models.Model):
    startup_profile = models.ForeignKey(StartupProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profilepage/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.startup_profile.startup_user.username} - {self.image.url}"