from django import forms
from django.contrib.auth.models import User
from Bombfunding.models import BaseUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# json files which forms must recieve (i guess)

class SignUpForm(UserCreationForm):
    pass

class LoginForm(AuthenticationForm):
    class Meta:
        model = BaseUser
        fields = ('username', 'password')