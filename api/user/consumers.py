import json
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.user.models import Token
from api.user.serializers import TokenSerializer


class UserConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.token_key = self.scope["token"]

        token = Token.objects.filter(key=self.token_key)
        if token.exists():
            self.token = token.first()
            self.token.is_active = True
            self.token.save()

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
            self.token.is_active = False
            self.token.save()

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_logout',
                    'token': self.token_key
                }
            )

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        token = text_data_json.get('token')
        status = text_data_json.get('status')

        if token and self.token:
            Token.objects.filter(key=token).update(is_active=False)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_logout',
                    'token': token
                }
            )
        elif status == 'login' and self.token:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_login',
                    'token': self.token_key
                }
            )

    async def user_login(self, event):
        data = event['token']
        t = Token.objects.get(key=data)

        token = Token.objects.filter(
            is_active=True,
            user_id=t.user.id
        )

        await self.send(text_data=json.dumps({
            'is_logged_in': True,
            'data': TokenSerializer(instance=token, many=True).data
        }))

    async def user_logout(self, event):
        token = event['token']

        if token == self.token_key:
            await self.send(text_data=json.dumps({
                'is_logged_in': False
            }))
        else:
            token = Token.objects.filter(
                is_active=True,
                user_id=self.token.user.id
            )
            await self.send(text_data=json.dumps({
                'is_logged_in': True,
                'data': TokenSerializer(instance=token, many=True).data
            }))