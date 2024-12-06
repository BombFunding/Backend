from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from authenticator.models import BaseUser
from .serializers import BaseUserSerializer
from .filters import BaseUserFilter

class BaseUserSearchView(generics.ListAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BaseUserFilter