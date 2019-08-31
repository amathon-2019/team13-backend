from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Token':
                    token = Token.objects.get(key=token_key)
                    scope['user'] = token.user
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()


        return self.inner(scope)

JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(
    AuthMiddlewareStack(inner)
)
