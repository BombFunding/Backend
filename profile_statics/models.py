from django.db import models
from authenticator.models import BaseUser
from datetime import date

class ProfileStatics(models.Model):
    user = models.OneToOneField(
        BaseUser,
        on_delete=models.CASCADE,
        related_name="profile_statics",
        limit_choices_to={"user_type__in": ["startup", "investor"]},
    )
    likes = models.JSONField(default=dict, blank=True)
    views = models.JSONField(default=dict, blank=True)

    def increment_view(self):
        today = date.today().isoformat()  
        if today in self.views:
            self.views[today] += 1  
        else:
            self.views[today] = 1  
        self.save()  

    def increment_like(self):
        today = date.today().isoformat()
        if today in self.likes:
            self.likes[today] += 1
        else:
            self.likes[today] = 1
        self.save()

    def decrement_like(self):
        today = date.today().isoformat()
        if today in self.likes:
            self.likes[today] -= 1
        else:
            self.likes[today] = -1
        self.save()


    class Meta:
        verbose_name = "Profile Statistic"
        verbose_name_plural = "Profile Statistics"

    def __str__(self):
        return f"Statistics for {self.user.username}"
