from django.db import models
from authenticator.models import BaseUser
from datetime import date

class ProfileStatics(models.Model):
    user = models.OneToOneField(
        BaseUser,
        on_delete=models.CASCADE,
        related_name="profile_statics",
        limit_choices_to={"user_type__in": ["startup"]},
    )
    likes = models.JSONField(default=dict, blank=True)
    views = models.JSONField(default=dict, blank=True)
    fund = models.JSONField(default=dict, blank=True)

    def increment_view(self):
        today = date.today().isoformat()  
        if today in self.views:
            self.views[today] += 1  
        else:
            self.views[today] = 1  
        self.save()  

    def add_like(self, liked_by_user):
        """
        Add a like entry with the current date and the user who liked.

        Args:
            liked_by_user (str): The username of the user who liked the profile.
        """
        today = date.today().isoformat()
        if today not in self.likes:
            self.likes[today] = []
        
        if liked_by_user not in self.likes[today]:
            self.likes[today].append(liked_by_user)
            self.save()


    def remove_like(self, liked_by_user):
        """
        Remove a like entry for the current date by a specific user.

        Args:
            liked_by_user (str): The username of the user who unliked the profile.
        """
        today = date.today().isoformat()
        if today in self.likes and liked_by_user in self.likes[today]:
            self.likes[today].remove(liked_by_user)
            if not self.likes[today]:
                del self.likes[today]  
        self.save()

    def increment_fund(self, amount):
        today = date.today().isoformat()
        if today in self.fund:
            self.fund[today] += amount
        else:
            self.fund[today] = amount
        self.save()
        
    class Meta:
        verbose_name = "Profile Statistic"
        verbose_name_plural = "Profile Statistics"

    def __str__(self):
        return f"Statistics for {self.user.username}"
    
    def is_liked_by(self, liked_by_username):
        """
        Check if a specific user has liked the profile at any time.

        Args:
            liked_by_username (str): The username of the user to check.

        Returns:
            bool: True if the user has liked the profile, False otherwise.
        """
        for day_likes in self.likes.values():
            if liked_by_username in day_likes:
                return True
        return False