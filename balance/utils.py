from authenticator.models import BaseUser
from rest_framework.exceptions import ValidationError

class UserBalanceMixin:
    def reduce_balance(self, user: BaseUser, amount: int):
        if user.balance < amount:
            raise ValidationError({
                "error": f"Insufficient balance. You have {user.balance} but {amount} is required."
            })
        user.balance -= amount
        user.save()
