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
    ),
    path("comment_on_profile/<int:profile_id>/", views.add_comment, name="add_comment"),
    path(
        "all_comments_of_profile/<int:profile_id>/",
        views.get_comments_by_profile,
        name="get_comments_by_profile",
    ),
    path(
        "delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"
    ),
    path("edit_comment/<int:comment_id>/", views.edit_comment, name="edit_comment"),
]
