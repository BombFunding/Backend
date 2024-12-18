from typing import Any
from django.db import models
from authenticator.models import BaseUser, StartupUser, BaseProfile
from position.models import Position
from django.core.exceptions import ValidationError


class StartupProfile(models.Model):
    startup_user = models.OneToOneField(
        StartupUser, on_delete=models.CASCADE, editable=False, null=True
    )
    startup_categories = models.CharField(
        max_length=50,
        choices=[
            ("Technology", "Technology"),
            ("Food", "Food"),
            ("Beauty", "Beauty"),
            ("Art", "Art"),
            ("Health", "Health"),
            ("Tourism", "Tourism"),
            ("Education", "Education"),
            ("Finance", "Finance"),
        ],
        default="Art",
    )
    score = models.IntegerField(default=0)
    startup_starting_date = models.DateField(null=True, blank=True)  
    startup_profile_visit_count = models.PositiveIntegerField(default=0)  


    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.startup_user.username}"



class StartupApplication(models.Model):
    startup_applicant = models.ForeignKey(BaseProfile, on_delete=models.CASCADE)
    investor_position = models.ForeignKey(
        "Bombfunding.InvestPosition",
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )

    def __str__(self) -> str:
        return f"{self.startup_applicant.name} - {self.investor_position.name}"


class StartupVote(models.Model):
    VOTE_CHOICES = (
        (1, "Upvote"),
        (-1, "Downvote"),
    )

    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    startup_profile = models.ForeignKey(StartupProfile, on_delete=models.CASCADE)
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ("user", "startup_profile")

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.startup_profile.score += self.vote
        else:
            old_vote = StartupVote.objects.get(pk=self.pk)
            self.startup_profile.score += self.vote - old_vote.vote
        self.startup_profile.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.startup_profile.score -= self.vote
        self.startup_profile.save()
        super().delete(*args, **kwargs)
