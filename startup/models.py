# آدما؟
# یه استارتاپیوزر چند تا پروفایل داشته باشه؟
# کامنت ادیت و حذف داره یا نه؟
# پیج خود جیسون پیجه ست
# درصد درآمد یا امتیاز
# پوزیشن های مختلف برای بخش های مختلف بتونه سرمایه گذاری کنه

from django.db import models
from Bombfunding.models import InvestPosition
from authenticator.models import StartupUser, BaseUser


class StartupProfile(models.Model):
    startup_user = models.OneToOneField(StartupUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, editable=False)  
    description = models.TextField()
    page = models.JSONField()
    categories = models.JSONField()

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.startup_user.username  
        super().save(*args, **kwargs)

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
        null=True,  
        default=None,  
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
        null=True,  
        default=None,  
    )

    def __str__(self) -> str:
        return f"{self.startup_applicant.name} - {self.investor_position.name}"