from channels.routing import ProtocolTypeRouter, URLRouter

from api.user import routing
from utils.auth import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
})
