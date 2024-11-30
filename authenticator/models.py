from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError as RestValidationError


class BaseUserManager(BaseUserManager):
    def create_user(self, username, email, password, user_type) -> "BaseUser":
        if not email:
            raise RestValidationError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, user_type=user_type, password=password
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, user_type):
        user = self.create_user(username, email, password, user_type)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseUser(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        ("investor", "Investor"),
        ("startup", "Startup"),
        ("basic", "Basic"),
    )

    username = models.CharField(default=" ", max_length=20, unique=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="basic"
    )
    is_confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    password = models.CharField(
        max_length=128,
        validators=[
            RegexValidator(
                regex=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$",
                message="Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a special character.",
                code="invalid_password",
            )
        ],
    )
    objects = BaseUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "password", "user_type"]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.full_clean()
            self.password = make_password(self.password)
        super(BaseUser, self).save(*args, **kwargs)

    def change_password(self, new_password):
        self.password = new_password
        self.full_clean()
        self.password = make_password(self.password)
        self.save()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self) -> str:
        return f"{self.username} - {self.user_type}"


class BasicUser(models.Model):
    username = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, primary_key=True
    )

    def __str__(self) -> str:
        return f"{self.username.__str__()}"


class InvestorUser(models.Model):
    username = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, primary_key=True
    )
    page = models.JSONField(null=True, blank=True)
    categories = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.username}"


class StartupUser(models.Model):
    username = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, primary_key=True
    )

    @property
    def display_username(self):
        return self.username.username

    def save(self, *args, **kwargs):
        if self.username:
            self.username = BaseUser.objects.get(pk=self.username.pk)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.username.username


from django.core.files.storage import default_storage
import os

def delete_existing_images(username):
    for ext in ["jpg", "jpeg", "png"]:
        file_path = os.path.join("profile_pics", f"{username}.{ext}")
        if default_storage.exists(file_path):
            default_storage.delete(file_path)

# TODO: Perhaps, we should move these functions to a separate file if they are used in multiple models.
# TODO: These two functions are also very similar. Perhaps, we can combine them into one function.

def user_profile_picture_path(instance, filename):
    username = instance.base_user.username
    file_extension = filename.split(".")[-1]
    new_filename = f"{username}.{file_extension}"
    file_path = os.path.join("profile_pics", new_filename)

    delete_existing_images(username)

    return file_path


def delete_existing_header_images(username):
    for ext in ["jpg", "jpeg", "png"]:
        file_path = os.path.join("header_pics", f"{username}.{ext}")
        if default_storage.exists(file_path):
            default_storage.delete(file_path)


def user_header_picture_path(instance, filename):
    username = instance.base_user.username
    file_extension = filename.split(".")[-1]
    new_filename = f"{username}.{file_extension}"
    file_path = os.path.join("header_pics", new_filename)

    delete_existing_header_images(username)

    return file_path

class BaseProfile(models.Model):
    base_user = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, editable=False
    )
    name = models.CharField(max_length=50, editable=False, null=True)
    email = models.EmailField(max_length=100, editable=False, null=True)
    socials = models.JSONField(default=dict, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True, default='profile_pics/default_profile.jpg')  
    header_picture = models.ImageField(upload_to=user_header_picture_path, null=True, blank=True, default='header_pics/default_header.jpg')  


    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.base_user.username
        if not self.email:
            self.email = self.base_user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.base_user.username}"


class BaseuserComment(models.Model):
    baseuser_profile = models.ForeignKey(BaseProfile, on_delete=models.CASCADE)
    username = models.ForeignKey(
        BaseUser,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )
    comment = models.TextField()
    time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.username} - {self.baseuser_profile.name}"


from django.db.models.signals import post_save
from django.dispatch import receiver
from startup.models import StartupProfile

@receiver(post_save, sender=BaseUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        base_profile = BaseProfile.objects.create(
            base_user=instance,
            name=instance.username,
            email=instance.email,
            bio="",
        )
        if instance.user_type == "startup": 
            startup_user = StartupUser.objects.create(username=instance)
            StartupProfile.objects.create(
                startup_user=startup_user,
                startup_categories="Technology",
                startup_starting_date=None,
                startup_rank=1,
                startup_profile_visit_count=0,
            )
        elif instance.user_type == "basic":
            BasicUser.objects.create(username=instance)
        elif instance.user_type == "investor":
            InvestorUser.objects.create(username=instance)
@receiver(post_delete, sender=BaseUser)
def delete_user_profile(sender, instance, **kwargs):
    """
    زمانی که یک BaseUser حذف می‌شود، پروفایل‌های مربوط به آن نیز حذف می‌شود.
    """
    try:
        from startup.models import BaseProfile

        if instance.user_type == "basic":
            instance.basic_user_profile.delete()
        elif instance.user_type == "investor":
            instance.investor_user.delete()
        elif instance.user_type == "startup":
            startup_user = instance.startup_user
            startup_user.delete()
            baseuser_profile = BaseProfile.objects.get(startup_user=startup_user)
            baseuser_profile.delete()
    except Exception as e:
        pass


