from django.urls import path

from . import views

urlpatterns = [
    path(
        "create_update_position/",
        views.create_update_position,
        name="create_update_position",
    ),
    path(
        "search_by_date_range/",
        views.search_positions_by_date_range,
        name="search_positions_by_date_range",
    ),
    path("all_positions/", views.get_all_positions, name="get_all_positions"),
    path(
        "positions/search_by_date_range/",
        views.search_positions_by_date_range,
        name="search_positions_by_date_range",
    ),
    path(
        "positions/sort_by_date/",
        views.sort_positions_by_date,
        name="sort_positions_by_date",
    ),
    path(
        "positions/sort_by_funded/",
        views.sort_positions_by_funded,
        name="sort_positions_by_funded",
    )
]
