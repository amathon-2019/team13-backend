import json
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.history.models import History
from apps.user.models import Token


class UserConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.token_key = self.scope["token"]

        token = Token.objects.filter(key=self.token_key)
        if token.exists():
            self.token = token.first()
            history, created = History.objects.get_or_create(
                token=self.token
            )
            history.is_active = True
            history.save()

            self.room_name = self.token.user.id
            self.room_group_name = 'user_{}'.format(self.room_name)

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        else:
            self.token = None

        await self.accept()

    async def disconnect(self, close_code):
        if self.token:
            history = History.objects.filter(
                token=self.token
            )
            if history.exists():
                history.is_active = False
                history.save()

                await self.channel_layer.group_discard(
                    self.room_group_name,
                    self.channel_name
                )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        device = text_data_json['device']

        if self.token:
            history = self.token.history 
            history.device = device
            history.save()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_logged_in',
                'token': self.token_key
            }
        )

    async def user_logged_in(self, event):
        token = event['token']

        if token != self.token_key:
            self.token.delete()
            await self.send(text_data=json.dumps({
                'is_logged_in': False
            }))