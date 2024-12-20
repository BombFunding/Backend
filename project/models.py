from django.db import models
from startup.models import StartupProfile
from authenticator.models import BaseUser

class Project(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="projects", limit_choices_to={"user_type__in": ["startup", "investor"]})
    page = models.JSONField(default=dict)
    name = models.CharField(max_length=50, default="Startup Project")
    image = models.ImageField(upload_to="projects/", default="header_pics/default_header.jpg")
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