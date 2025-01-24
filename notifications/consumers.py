import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.token = self.scope['url_route']['kwargs']['token']
        self.user = await self.get_user_from_token(self.token)
        if (self.user):
            await self.channel_layer.group_add(
                str(self.user.id),
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def receive(self, text_data):
        # Handle incoming messages if needed
        pass

    async def notification_message(self, event):
        await self.send(text_data=json.dumps(event["content"]))

    async def disconnect(self, close_code):
        if self.user:
            await self.channel_layer.group_discard(
                str(self.user.id),
                self.channel_name
            )

    async def get_user_from_token(self, token):
        User = get_user_model()
        try:
            validated_token = UntypedToken(token)
            user_id = validated_token["user_id"]
            return await User.objects.aget(id=user_id)
        except (InvalidToken, TokenError, KeyError, User.DoesNotExist):
            return None

class HelloWorldConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(json.dumps({"message": "Hello World"}))