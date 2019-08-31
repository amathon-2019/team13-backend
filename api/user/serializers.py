from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.user.models import User
from apps.history.models import History
from apps.history.enums import DeviceType


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    device = serializers.ChoiceField(
        choices=DeviceType.choices()
    )

    def login(self):
        user = authenticate(
            username=self.validated_data['username'],
            password=self.validated_data['password']
        )
        if user is not None:
            History.objects.create(**{
                'user': user,
                'device': self.validated_data['device']
            })

        return user


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                "이미 가입된 아이디입니다."
            )
        return data

    def save(self):
        user = User(
            username=self.validated_data['username']
        )
        user.set_password(self.validated_data['password'])
        user.save()

        return user


class DuplicateSerializer(serializers.Serializer):
    username = serializers.CharField()

    def is_duplicate(self):
        return User.objects.filter(
            username=self.validated_data['username']
        ).exists()
