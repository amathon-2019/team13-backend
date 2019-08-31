from urllib import parse
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header,
)
from rest_framework import exceptions


from apps.user.models import Token


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        query_string = scope.get('query_string')
        query_string = dict(parse.parse_qsl(query_string))

        token_key = query_string.get(b'token')
        if token_key:
            token_key = token_key.decode()
        
        try:
            token = Token.objects.get(key=token_key)
            
            print(token)

            if token.expired > timezone.now():
                scope['user'] = token.user
                scope['token'] = token.key
            else:
                token.is_active = False
                token.save()
                scope['user'] = AnonymousUser()
                scope['token'] = None
        except Token.DoesNotExist:
            scope['user'] = AnonymousUser()
            scope['token'] = None

        return self.inner(scope)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(
    AuthMiddlewareStack(inner)
)


class TokenAuthentication(BaseAuthentication):
    keyword = 'Bearer'

    def get_model(self):
        return Token

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = "잘못된 인증 헤더입니다"
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = "잘못된 인증 헤더입니다. 토큰은 공백이 없어야합니다."
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = "잘못된 인증 헤더입니다. 토큰에 잘못된 문자열이 들어가 있습니다."
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed("잘못된 토큰")

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed("유저가 비활성화 되어 있거나 존재하지 않습니다.")

        return (token.user, token)

    def authenticate_header(self, request):
        return self.keyword