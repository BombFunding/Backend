from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class AuthTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Test123456!',
            user_type='basic'
        )
        self.user.is_confirmed = True
        self.user.save()

    def test_login_success(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'Test123456!'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_login_invalid_credentials(self):
        url = reverse('login')  # Adjust the URL name as per your urls.py
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forget_password_email_success(self):
        url = reverse('forgetpassword')  # Adjust the URL name as per your urls.py
        data = {
            'email': 'testuser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Email sent')

    def test_forget_password_email_non_existent_user(self):
        url = reverse('forgetpassword')  # Adjust the URL name as per your urls.py
        data = {
            'email': 'nonexistent@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)