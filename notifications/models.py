from django.db import models

# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey("authenticator.BaseUser", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    type = models.CharField(max_length=255, default="generic-notification")

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

def send_notification(user, message, type):
    Notification.objects.create(user=user, message=message, type=type)

def send_investment_notification(investor, position_owner, investment_amount):
    message = f"مبلغ {investment_amount} توسط {investor.username} به حساب شما اضافه شد."
    send_notification(position_owner, message, "investment-notification")
