from typing import Any
from django.db import models
from authenticator.models import BaseUser, InvestorUser, BaseProfile
from django.core.exceptions import ValidationError


class InvestorProfile(models.Model):
    investor_user = models.OneToOneField(
        InvestorUser, on_delete=models.CASCADE, editable=False, null=True
    )
    score = models.IntegerField(default=0)
    investor_starting_date = models.DateField(null=True, blank=True)
    investor_profile_visit_count = models.PositiveIntegerField(default=0)

    national_id = models.CharField(max_length=10, verbose_name="National ID",blank=True)
    legal_code = models.CharField(max_length=15, verbose_name="Legal Code", null=True, blank=True)
    iban = models.CharField(max_length=34, verbose_name="IBAN", null=True, blank=True)
    tax_identification_number = models.CharField(
        max_length=20, verbose_name="Tax Identification Number", null=True, blank=True
    )
    address = models.TextField(verbose_name="Address", null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.investor_user.username}"


class InvestorVote(models.Model):
    VOTE_CHOICES = (
        (1, "like"),
        (0, "nothing"),
    )

    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    investor_profile = models.ForeignKey(InvestorProfile, on_delete=models.CASCADE)
    vote = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ("user", "investor_profile")

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.investor_profile.score += self.vote
        else:
            old_vote = InvestorVote.objects.get(pk=self.pk)
            self.investor_profile.score += self.vote - old_vote.vote
        self.investor_profile.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.investor_profile.score -= self.vote
        self.investor_profile.save()
        super().delete(*args, **kwargs)
