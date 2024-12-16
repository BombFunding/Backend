from .models import StartupUser
from authenticator.utils import get_instance

def is_startup_user(user_id: int):
    startup_user = get_instance(StartupUser, username=user_id)
    if not startup_user:
        return False
    return True

