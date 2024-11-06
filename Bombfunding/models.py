
from django.db import models
from authenticator.models import InvestorUser


class InvestPosition(models.Model):
    username = models.ForeignKey(InvestorUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    total = models.IntegerField()
    available = models.IntegerField()
    is_done = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.name} - {self.username} {self.available}/{self.total}"


class InvestorApplication(models.Model):
    investor_applicant = models.ForeignKey(InvestorUser, on_delete=models.CASCADE)
    investor_position = models.ForeignKey(
        'Bombfunding.InvestPosition',
        on_delete=models.CASCADE,
        null=True,  
        default=None,  
    )

    def __str__(self) -> str:
        return f"{self.investor_applicant.username} - {self.startup_position.name}"