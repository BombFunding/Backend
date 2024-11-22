from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from authenticator.models import BaseUser, StartupUser, InvestorUser, BasicUser


class InvestPosition(models.Model):
    username = models.ForeignKey(InvestorUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField
    total = models.IntegerField()
    available = models.IntegerField()
    is_done = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.name} - {self.username} {self.available}/{self.total}"


class StartupProfile(models.Model):
    startup_user = models.OneToOneField(StartupUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    page = models.JSONField()
    categories = models.JSONField

    def __str__(self) -> str:
        return f"{self.name} - {self.startup_user.username}"

class StartupPosition(models.Model):
    startup_profile = models.ForeignKey(StartupProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    total = models.IntegerField()
    funded = models.IntegerField()
    is_done = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.name} - {self.startup_profile.name} {self.funded}/{self.total}"

class StartupComment(models.Model):
    startup_profile = models.ForeignKey(StartupProfile, on_delete=models.CASCADE)
    username = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    comment = models.TextField()
    time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.username} - {self.startup_profile.name}"

class InvestorApplication(models.Model):
    investor_applicant = models.ForeignKey(InvestorUser, on_delete=models.CASCADE)
    startup_position = models.ForeignKey(StartupPosition, on_delete=models.CASCADE)

class StartupApplication(models.Model):
    startup_applicant = models.ForeignKey(StartupProfile, on_delete=models.CASCADE)
    investor_position = models.ForeignKey(InvestPosition, on_delete=models.CASCADE)