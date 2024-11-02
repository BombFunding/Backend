from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class BaseUserManager(BaseUserManager):
    def create_user(self, username, email, password=None) -> 'BaseUser':
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class BaseUser(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        ('Investor', 'Investor'),
        ('Startup', 'Startup'),
        ('Basic', 'Basic'),
    )

    username = models.CharField(default=" ",max_length=20, unique=True)
    email = models.EmailField()
    name = models.CharField(default=" ",max_length=50)
    about_me = models.TextField(default=" ")
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="Basic")

    password = models.CharField(
        max_length=128,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                message="Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a special character."
            )
        ]
    )
    objects = BaseUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']
    
    def save(self, *args, **kwargs):
        if not self.pk:  
            self.password = make_password(self.password)
        super(BaseUser, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return f"{self.name} - {self.user_type}"
