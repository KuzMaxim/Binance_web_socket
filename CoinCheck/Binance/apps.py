from django.apps import AppConfig


class BinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Binance'

    def ready(self):
        from .binapi import run
        run()
