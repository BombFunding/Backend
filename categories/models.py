from django.db import models
from authenticator.models import BaseUser
from project.models import CATEGORIES

class LikedSubcategories(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="liked_subcategories")
    subcategories = models.JSONField(default=list)

    def add_subcategory(self, subcategory):
        if subcategory not in self.subcategories:
            self.subcategories.append(subcategory)
            self.save()

    def remove_subcategory(self, subcategory):
        if subcategory in self.subcategories:
            self.subcategories.remove(subcategory)
            self.save()

    def __str__(self) -> str:
        return f"{self.user.username} - {self.subcategory.name}"