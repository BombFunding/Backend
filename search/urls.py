from django.urls import path
from .views import CombinedSearchView

urlpatterns = [
    # path("search/", CombinedSearchView.as_view(), name="search"),
    path("search/<str:query>/", CombinedSearchView.as_view(), name="search-with-query"),
]
