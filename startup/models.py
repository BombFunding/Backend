from django.db import models
from authenticator.models import BaseUser, StartupUser,BaseProfile

class StartupProfile(models.Model):
    base_profile = models.OneToOneField(
        BaseProfile, on_delete=models.CASCADE, editable=False
    )
    startup_rank = models.IntegerField(default=0)  
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
        default="Technology",
    )  
    startup_starting_date = models.DateField(null=True, blank=True)  
    startup_profile_visit_count = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.base_profile.name}"


class StartupPosition(models.Model):
    startup_profile = models.ForeignKey(BaseProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    bio = models.TextField()
    total = models.IntegerField()
    funded = models.IntegerField()
    is_done = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.name} - {self.startup_profile.name} {self.funded}/{self.total}"


class StartupComment(models.Model):
    startup_profile = models.ForeignKey(BaseProfile, on_delete=models.CASCADE)
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
    startup_applicant = models.ForeignKey(BaseProfile, on_delete=models.CASCADE)
    investor_position = models.ForeignKey(
        "Bombfunding.InvestPosition",
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )

    def __str__(self) -> str:
        return f"{self.startup_applicant.name} - {self.investor_position.name}"
