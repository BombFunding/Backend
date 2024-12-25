from django.db import models
from startup.models import StartupProfile
from authenticator.models import BaseUser

class Project(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="projects", limit_choices_to={"user_type__in": ["startup"]})
    page = models.JSONField(default=dict)
    name = models.CharField(max_length=50, default="Startup Project")
    image = models.ImageField(upload_to="projects/", default="projects/default_project.jpg")
    description = models.TextField(max_length=500, blank=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ("Technology", "Technology"),
            ("Art", "Art"),
            ("Wellness", "Wellness"),
            ("Tourism", "Tourism"),
            ("Education", "Education"),
            ("Finance", "Finance"),
        ],
        default="Art",
    )

class ProjectImage(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projectimages/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.image.url}"