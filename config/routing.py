from channels.routing import ProtocolTypeRouter, URLRouter

from api.user import routing
from utils.auth import JWTAuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': JWTAuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
})
