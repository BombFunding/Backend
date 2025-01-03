from django.db import models
from authenticator.models import BaseUser

CATEGORIES = {
    # "Technology": ["Artificial Intelligence", "Internet of Things", "Software", "Security", "Augmented Reality"],
    "تکنولوژی": ["هوش مصنوعی", "اینترنت اشیا", "نرم‌افزار", "امنیت", "واقعیت افزوده"],
    # "Art": ["Music", "Cinema", "Handicrafts"],
    "هنری": ["موسیقی", "سینما", "صنایع دستی"],
    # "Wellness": ["Nutrition", "Psychology", "Therapy"],
    "سلامت": ["تغذیه", "روان", "درمان"],
    # "Tourism": ["Cultural", "Urban", "International"],
    "گردشگری": ["فرهنگی", "شهری", "بین‌المللی"],
    # "Education": ["Books and Publications", "Personal Development", "Educational Institutions"],
    "آموزش": ["کتاب و نشریات", "توسعه فردی", "آموزشگاه"],
    # "Finance": ["Investment Fund", "Cryptocurrency", "Insurance"],
    "مالی": ["سرمایه گذاری", "ارز دیجیتال", "بیمه"],
}

class Project(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name="projects", limit_choices_to={"user_type__in": ["startup"]})
    page = models.JSONField(default=dict)
    name = models.CharField(max_length=50, default="Startup Project")
    image = models.ImageField(upload_to="projects/", default="projects/default_project.jpg")
    description = models.TextField(max_length=500, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    subcategories = models.JSONField(default=list, blank=True)

class ProjectImage(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projectimages/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.image.url}"