from django.db import models
from authenticator.models import BaseUser
from position.models import Position

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