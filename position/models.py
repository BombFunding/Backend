from django.db import models
from authenticator.models import BaseUser

from django.db import models
from django.contrib.postgres.fields import ArrayField  

class Position(models.Model):
    TECHNOLOGY_CHOICES = [
        ("Artificial Intelligence", "Artificial Intelligence"),
        ("Internet of Things", "Internet of Things"),
        ("Software", "Software"),
        ("Security", "Security"),
        ("Augmented Reality", "Augmented Reality"),
    ]

    ART_CHOICES = [
        ("Music", "Music"),
        ("Cinema", "Cinema"),
        ("Handicrafts", "Handicrafts"),
    ]

    HEALTH_CHOICES = [
        ("Nutrition", "Nutrition"),
        ("Psychology", "Psychology"),
        ("Therapy", "Therapy"),
    ]

    TOURISM_CHOICES = [
        ("Cultural", "Cultural"),
        ("Urban", "Urban"),
        ("International", "International"),
    ]

    EDUCATION_CHOICES = [
        ("Books and Publications", "Books and Publications"),
        ("Personal Development", "Personal Development"),
        ("Educational Institutions", "Educational Institutions"),
    ]

    FINANCE_CHOICES = [
        ("Investment Fund", "Investment Fund"),
        ("Cryptocurrency", "Cryptocurrency"),
        ("Insurance", "Insurance"),
    ]

    CATEGORY_CHOICES = TECHNOLOGY_CHOICES + ART_CHOICES + HEALTH_CHOICES + TOURISM_CHOICES + EDUCATION_CHOICES + FINANCE_CHOICES

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

    
    subcategory = ArrayField(
        models.CharField(max_length=100, choices=CATEGORY_CHOICES),
        blank=True,  
        default=list  
    )

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