from startup.models import StartupProfile
from .models import Team, TeamMember
from authenticator.models import BaseUser


class RetrieveInstanceMixin:
    def get_instance(self, model, **lookup):
        try:
            instance = model.objects.get(**lookup)
            return instance
        except model.DoesNotExist:
            return None


class TeamMixin(RetrieveInstanceMixin):
    def get_team(self, startup_user):
        return self.get_instance(Team, startup_user=startup_user)

    def get_team_member(self, user, team):
        return self.get_instance(TeamMember, user=user, team=team)

    def is_user_in_team(self, user, team):
        return TeamMember.objects.filter(user=user, team=team).exists()

class UserFromUsernameMixin(RetrieveInstanceMixin):
    def get_user(self, username):
        return self.get_instance(BaseUser, username=username)
