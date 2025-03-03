from django.urls import path, include
from Binance.routing import websocket_urlpatterns
from . import views

urlpatterns = [
    path('', views.index),
]