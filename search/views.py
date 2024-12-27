from rest_framework.views import APIView
from rest_framework.response import Response
from authenticator.models import BaseUser
from startup.models import StartupUser
from project.models import Project
from .serializers import BaseUserSerializer, StartupSerializer, ProjectSerializer

class CombinedSearchView(APIView):
    def get(self, request, query=None):
        if not query:
            query = request.GET.get('q', '')

        users = BaseUser.objects.filter(username__icontains=query)
        startups = StartupUser.objects.filter(username__username__icontains=query)
        projects = Project.objects.filter(name__icontains=query)

        return Response({
            'users': BaseUserSerializer(users, many=True).data,
            'startups': StartupSerializer(startups, many=True).data,
            'projects': ProjectSerializer(projects, many=True).data
        })