from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from Bombfunding.models import BaseUser

# json files which forms must recieve (i guess)


class SignUpForm(UserCreationForm):
    pass


class LoginForm(AuthenticationForm):
    class Meta:
        model = BaseUser
        fields = ("username", "password")
