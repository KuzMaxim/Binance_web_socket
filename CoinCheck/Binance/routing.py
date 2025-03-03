from django.urls import re_path
from Binance.consumers import TickerConsumer
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/socket-server', TickerConsumer.as_asgi()),
    ]