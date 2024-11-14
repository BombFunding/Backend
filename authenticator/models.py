from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as RestValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

class BaseUserManager(BaseUserManager):
    def create_user(self, username, email, password, user_type) -> 'BaseUser':
        if not email:
            raise RestValidationError("Email is required.")
        email = self.normalize_email(email)

        password_field = BaseUser._meta.get_field("password")
        try:
            for validator in password_field.validators:
                validator(password)
        except DjangoValidationError as e:
            raise RestValidationError({"password": e.messages})

        user = self.model(username=username, email=email, user_type=user_type)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, user_type):
        user = self.create_user(username, email, password, user_type)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)  
        user.save(using=self._db)
        return user

class BaseUser(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        ('investor', 'Investor'),
        ('startup', 'Startup'),
        ('basic', 'Basic'),
    )

    username = models.CharField(default=" ", max_length=20, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(default=" ", max_length=50)
    about_me = models.TextField(default=" ")
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="basic")
    is_confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    password = models.CharField(
        max_length=128,
        validators=[ 
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$',
                message="Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a special character.",
                code="invalid_password"
            )
        ]
    )
    objects = BaseUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password', 'user_type']

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.password = make_password(self.password)
        super(BaseUser, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self) -> str:
        return f"{self.name} - {self.user_type}"

class BasicUser(models.Model):
    username = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self) -> str:
        return f"{self.username}"

class InvestorUser(models.Model):
    username = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)
    page = models.JSONField(null=True, blank=True)
    categories = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.username}"

class StartupUser(models.Model):
    username = models.OneToOneField(BaseUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self) -> str:
        return f"{self.username}"

@receiver(post_save, sender=BaseUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "basic":
            BasicUser.objects.create(username=instance)
        elif instance.user_type == "investor":
            InvestorUser.objects.create(username=instance)
        elif instance.user_type == "startup":
            startup_user = StartupUser.objects.create(username=instance)

            from startup.models import StartupProfile  

            StartupProfile.objects.create(
                startup_user=startup_user,
                name=instance.username,  
                description="",          
                page={},                 
                categories=[],           
            )
