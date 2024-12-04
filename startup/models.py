from django.db import models
from authenticator.models import BaseUser, StartupUser,BaseProfile

from django.core.exceptions import ValidationError

class StartupProfile(models.Model):
    startup_user = models.OneToOneField(
        StartupUser, on_delete=models.CASCADE, editable=False , null=True
    )
    startup_rank = models.PositiveSmallIntegerField(default=1)  
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
    startup_starting_date = models.DateField(null=True, blank=True)  
    startup_ending_date = models.DateField(null=True, blank=True)  
    startup_profile_visit_count = models.PositiveIntegerField(default=0)  

    def clean(self):
        if not (1 <= self.startup_rank <= 5):
            raise ValidationError({'startup_rank': "Rank must be between 1 and 5."})

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.startup_user.username}"


    @property
    def positions(self):
        return StartupPosition.objects.filter(startup_profile=self)



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
        return f"{self.name} - {self.startup_profile.startup_user.username} {self.funded}/{self.total}"

    @property
    def positions(self):
        return StartupPosition.objects.filter(startup_profile=self)


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
