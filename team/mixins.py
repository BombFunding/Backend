from startup.models import StartupUser
from .models import Team, TeamMember
from authenticator.models import BaseUser
from startup.utils import is_startup_user
from rest_framework.exceptions import ValidationError


class RetrieveInstanceMixin:
    def get_instance(self, model, **lookup):
        try:
            instance = model.objects.get(**lookup)
            return instance
        except model.DoesNotExist:
            return None


class TeamMixin(RetrieveInstanceMixin):
    def get_team(self, user_id):
        startup_user = self.get_instance(StartupUser, username=user_id)
        if not is_startup_user(user_id):
            raise ValidationError({"error": "The specified user is not a startup user."})
        return self.get_instance(Team, startup_user=startup_user)

    def get_team_member(self, user, team):
        return self.get_instance(TeamMember, user=user, team=team)

    def is_user_in_team(self, user, team):
        return TeamMember.objects.filter(user=user, team=team).exists()

class UserFromUsernameMixin(RetrieveInstanceMixin):
    def get_user(self, username):
        return self.get_instance(BaseUser, username=username)
