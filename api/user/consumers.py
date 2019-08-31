import json
from channels.generic.websocket import WebsocketConsumer
from apps.history.models import History
from apps.user.models import Token


class UserConsumers(WebsocketConsumer):
    def connect(self):
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
        else:
            self.token = None

        self.accept()

    def disconnect(self, close_code):
        if self.token:
            history = History.objects.filter(
                token=self.token
            )
            if history.exists():
                history.is_active = False
                history.save()

    def receive(self, text_data):
        pass