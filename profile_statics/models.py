from django.db import models
from authenticator.models import BaseUser


class ProfileStatics(models.Model):
    user = models.OneToOneField(
        BaseUser,
        on_delete=models.CASCADE,
        related_name="profile_statics",
        limit_choices_to={"user_type__in": ["startup", "investor"]},
    )
    likes = models.JSONField(
        default=dict,  
        blank=True,
        help_text="Dictionary of dates and like counts. Example: {'2024-12-01': 10, '2024-12-02': 5}",
    )
    views = models.JSONField(
        default=dict,  
        blank=True,
        help_text="Dictionary of dates and view counts. Example: {'2024-12-01': 15, '2024-12-02': 8}",
    )

    class Meta:
        verbose_name = "Profile Statistic"
        verbose_name_plural = "Profile Statistics"

    def __str__(self):
        return f"Statistics for {self.user.username}"

    def add_like(self, date):
        """ add like with specefic date"""
        self.likes[date] = self.likes.get(date, 0) + 1
        self.save()

    def add_view(self, date):
        """ add view with specefic date"""
        self.views[date] = self.views.get(date, 0) + 1
        self.save()
