# from django.contrib.postgres.search import SearchVector
from django_filters import rest_framework as filters
from authenticator.models import BaseUser
from startup.models import StartupProfile

class BaseUserFilter(filters.FilterSet):
    search = filters.CharFilter(method="search_filter")

    class Meta:
        model = BaseUser
        fields = ["search"]

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            username__icontains=value
        ) | queryset.filter(
            startupuser__startupprofile__startup_categories__icontains=value
        )