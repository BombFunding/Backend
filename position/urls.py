from django.urls import path, include
from .views import (
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    PositionListView,  
)

urlpatterns = [
    path("position/create/", PositionCreateView.as_view(), name="create_startup_position"),
    path("position/update/<int:position_id>/", PositionUpdateView.as_view(), name="update_startup_position"),
    path("position/delete/<int:position_id>/", PositionDeleteView.as_view(), name="delete_startup_position"),
    path("position/list/<str:username>/", PositionListView.as_view(), name="list_startup_positions"),  
]
