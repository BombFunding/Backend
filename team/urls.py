from django.urls import path

from . import views

urlpatterns = [
    path("add/", views.AddTeamMember.as_view(), name="add_team_member"),
    path("remove/<int:user>/", views.RemoveTeamMember.as_view(), name="remove_team_member"),
    path("update/<str:user>/", views.UpdateTeamMember.as_view(), name="edit_team_member"),
    path("list/", views.ListTeamMembers.as_view(), name="list_team_members"),
]
