from django.test import TestCase
from .models import Notification, send_notification
from django.contrib.auth import get_user_model

class NotificationTests(TestCase):
    def test_send_notification(self):
        user_model = get_user_model()
        user = user_model.objects.create(username="testuser", email="test@example.com", password="testpass")
        send_notification(user, "Hello World")
        self.assertEqual(Notification.objects.count(), 1)

# Create your tests here.
