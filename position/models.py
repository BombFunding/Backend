from django.db import models
from authenticator.models import BaseUser

class Position(models.Model):
    position_user = models.ForeignKey(
        BaseUser,
        on_delete=models.CASCADE,
        limit_choices_to={"user_type__in": ["startup", "investor"]},
    )
    name = models.CharField(max_length=50)
    description = models.TextField()
    total = models.IntegerField()
    funded = models.IntegerField()
    is_done = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.name} - {self.position_user.username}"


class Transaction(models.Model):
    investor_user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="transactions")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="transactions")
    investment_amount = models.DecimalField(max_digits=12, decimal_places=2)
    investment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction by {self.investor_user.username} on {self.position.name} for {self.investment_amount} at {self.investment_date}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"