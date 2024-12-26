from django.db import models
from project.models import Project

from authenticator.models import BaseUser


class Bookmark(models.Model):
    owner = models.ForeignKey(
        BaseUser, on_delete=models.CASCADE, related_name="bookmarks"
    )
    target = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["owner", "target"]
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"
