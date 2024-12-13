from django.db import models

from authenticator.models import BaseUser


class BookmarkUser(models.Model):
    owner = models.ForeignKey(
        BaseUser, on_delete=models.CASCADE, related_name="bookmarks"
    )
    target = models.ForeignKey(BaseUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["owner", "target"]
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"
