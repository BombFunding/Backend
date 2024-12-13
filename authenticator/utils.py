from .models import BaseUser
from rest_framework.exceptions import ValidationError

def get_instance(model, **lookup):
    try:
        instance = model.objects.get(**lookup)
        return instance
    except model.DoesNotExist:
        return None


def get_user_id_from_username(username: str):
    user = get_instance(BaseUser, username=username)
    if not user:
        raise ValidationError({"error": f"User with username {username} doesn't exist"})
    return user.id
