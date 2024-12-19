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
