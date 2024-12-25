from django.db import models
from authenticator.models import BaseUser
from project.models import Project  # Import the Project model

class Position(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="positions"
    )
    description = models.TextField(default="")
    total = models.IntegerField()
    funded = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()

    @property
    def is_done(self):
        return self.total == self.funded

    @property
    def is_closed(self):
        from django.utils import timezone
        return self.end_time < timezone.now()

    def __str__(self) -> str:
        return f"Position for project {self.project.name}"

class Transaction(models.Model):
    investor_user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="transactions")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="transactions")
    investment_amount = models.DecimalField(max_digits=12, decimal_places=2)
    investment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction by {self.investor_user.username} on position {self.position.id} for {self.investment_amount} at {self.investment_date}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"