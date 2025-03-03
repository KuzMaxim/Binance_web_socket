import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter#type: ignore
from channels.auth import AuthMiddlewareStack#type:ignore
import Binance.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CoinCheck.settings')

application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket' : AuthMiddlewareStack(
        URLRouter(
            Binance.routing.websocket_urlpatterns
        )
    )
    })