import os

from django.core.files.storage import default_storage
from django.db import models

from authenticator.models import BaseUser, StartupUser


def delete_existing_images(username):
    for ext in ["jpg", "jpeg", "png"]:
        file_path = os.path.join("profile_pics", f"{username}.{ext}")
        if default_storage.exists(file_path):
            default_storage.delete(file_path)


def user_profile_picture_path(instance, filename):
    username = instance.startup_user.username.username
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
    username = instance.startup_user.username.username
    file_extension = filename.split(".")[-1]
    new_filename = f"{username}.{file_extension}"
    file_path = os.path.join("header_pics", new_filename)

    delete_existing_header_images(username)

    return file_path


class StartupProfile(models.Model):
    startup_user = models.OneToOneField(
        StartupUser, on_delete=models.CASCADE, editable=False
    )
    name = models.CharField(max_length=50, editable=False, null=True)
    email = models.EmailField(max_length=100, editable=False, null=True)
    socials = models.JSONField(default=dict, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    bio = models.TextField(null=True, blank=True)
    page = models.JSONField(null=True, blank=True)
    categories = models.JSONField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to=user_profile_picture_path,
        null=True,
        blank=True,
        default="profile_pics/default_profile.jpg",
    )
    header_picture = models.ImageField(
        upload_to=user_header_picture_path,
        null=True,
        blank=True,
        default="header_pics/default_header.jpg",
    )

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.startup_user.username
        if not self.email:
            self.email = self.startup_user.username.email
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} - {self.startup_user.username}"


class StartupPosition(models.Model):
    startup_profile = models.ForeignKey(StartupProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    bio = models.TextField()
    total = models.IntegerField()
    funded = models.IntegerField()
    is_done = models.BooleanField(default=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.name} - {self.startup_profile.name} {self.funded}/{self.total}"


class StartupComment(models.Model):
    startup_profile = models.ForeignKey(StartupProfile, on_delete=models.CASCADE)
    username = models.ForeignKey(
        BaseUser,
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )
    comment = models.TextField()
    time = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.username} - {self.startup_profile.name}"


class StartupApplication(models.Model):
    startup_applicant = models.ForeignKey(StartupProfile, on_delete=models.CASCADE)
    investor_position = models.ForeignKey(
        "Bombfunding.InvestPosition",
        on_delete=models.CASCADE,
        null=True,
        default=None,
    )

    def __str__(self) -> str:
        return f"{self.startup_applicant.name} - {self.investor_position.name}"
