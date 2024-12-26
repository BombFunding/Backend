from django.urls import path
from .views import (
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    PositionDetailView,
    PositionExtendView,
)

urlpatterns = [
    path("create/<int:project_id>/", PositionCreateView.as_view(), name="create_position"),
    path("update/<int:id>/", PositionUpdateView.as_view(), name="update_position"),
    path("delete/<int:id>/", PositionDeleteView.as_view(), name="delete_position"),
    path("detail/<int:id>/", PositionDetailView.as_view(), name="detail_position"),
    path("extend/<int:position_id>/", PositionExtendView.as_view(), name="extend_position"),
]


