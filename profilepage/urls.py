from django.urls import path
from .views import ImageView

urlpatterns = [
    path("startup_image/<int:startup_profile_id>", ImageView.as_view(), name="image"),
]