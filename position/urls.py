from django.urls import path
from .views import (
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
    PositionListView,
    PositionRenewView,  
    PositionCostView,
)

urlpatterns = [
    path("create/", PositionCreateView.as_view(), name="create_startup_position"),
    path("update/<int:position_id>/", PositionUpdateView.as_view(), name="update_startup_position"),
    path("delete/<int:position_id>/", PositionDeleteView.as_view(), name="delete_startup_position"),
    path("list/<str:username>/", PositionListView.as_view(), name="list_startup_positions"),
    path("renew/<int:position_id>/", PositionRenewView.as_view(), name="renew_startup_position"),  
    path('costs/', PositionCostView.as_view(), name='position_costs'),
]
