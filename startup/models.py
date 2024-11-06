# startup/models.py
from django.db import models
from Bombfunding.models import InvestPosition
from authenticator.models import StartupUser, BaseUser


class StartupProfile(models.Model):
    startup_user = models.OneToOneField(StartupUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    page = models.JSONField()
    categories = models.JSONField()

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
    username = models.ForeignKey(
        BaseUser,
        on_delete=models.CASCADE,
        null=True,  # اجازه می‌دهیم این فیلد خالی باشد
        default=None,  # مقدار پیش‌فرض برای زمانی که فیلد خالی باشد
    )
    comment = models.TextField()
    time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.username} - {self.startup_profile.name}"

class StartupApplication(models.Model):
    startup_applicant = models.ForeignKey(StartupProfile, on_delete=models.CASCADE)
    investor_position = models.ForeignKey(
        'Bombfunding.InvestPosition',
        on_delete=models.CASCADE,
        null=True,  # این فیلد ممکن است خالی باشد
        default=None,  # مقدار پیش‌فرض که می‌توانید به طور دستی تنظیم کنید
    )

    def __str__(self) -> str:
        return f"{self.startup_applicant.name} - {self.investor_position.name}"
