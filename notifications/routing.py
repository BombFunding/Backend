from django.urls import path
from .consumers import NotificationConsumer, HelloWorldConsumer

websocket_urlpatterns = [
    path("ws/notifications/<str:token>/", NotificationConsumer.as_asgi()),
]

websocket_urlpatterns += [
    path("ws/helloworld/", HelloWorldConsumer.as_asgi()),
]