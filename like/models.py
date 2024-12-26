from django.db import models
from authenticator.models import BaseUser
from project.models import Project

class Like(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='likes')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.project.name}"
