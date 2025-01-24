from django.urls import path
from .views import UserNotificationsView, ReadNotificationView

urlpatterns = [
    path("user-notifications/", UserNotificationsView.as_view(), name="user-notifications"),
    path("read-notification/<int:pk>/", ReadNotificationView.as_view(), name="read-notification"),
]
