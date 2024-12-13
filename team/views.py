from rest_framework import generics
from .models import TeamMember
from .serializers import TeamMemberSerializer, TeamMemberListSerializer, TeamMemberUpdateSerializer
from rest_framework import permissions
from .mixins import TeamMixin
from .permissions import IsStartupOwner


class TeamSerializerContextMixin(TeamMixin):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        context["team"] = self.get_team(self.request.user)
        return context


class TeamQuerysetMixin:
    def get_queryset(self):
        team = self.get_team(self.request.user)
        return TeamMember.objects.filter(team=team)


class AddTeamMember(TeamSerializerContextMixin, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStartupOwner]
    serializer_class = TeamMemberSerializer


class ListTeamMembers(TeamQuerysetMixin, TeamMixin, generics.ListAPIView):
    serializer_class = TeamMemberListSerializer


class RemoveTeamMember(TeamMixin, TeamQuerysetMixin, generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStartupOwner]
    serializer_class = TeamMemberSerializer
    lookup_field = "user"


class UpdateTeamMember(TeamSerializerContextMixin, TeamQuerysetMixin, TeamMixin, generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStartupOwner]
    serializer_class = TeamMemberUpdateSerializer
    lookup_field = "user"