from django.utils import timezone
from .models import Position

def has_open_position(project):
    """
    Check if the given project has an open position.
    """
    return Position.objects.filter(project=project, end_time__gt=timezone.now()).exists()

def get_open_position(project):
    """
    Get the open position of the given project.
    """
    return Position.objects.filter(project=project, end_time__gt=timezone.now()).first()
