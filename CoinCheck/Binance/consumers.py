import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer  # type: ignore
from .models import Crypto


class TickerConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active = True
        self.db = Crypto()
        self.ticker = "BTC"

    async def connect(self):
        await self.accept()

        asyncio.create_task(self.send_periodic_updates())

    async def disconnect(self):
        self.active = False


    async def send_periodic_updates(self):
        while self.active:
            await asyncio.sleep(5)
            try:
                price = await self.db.get(self.ticker)
                await self.send(text_data=json.dumps({
                    'message': f"Обновлённая цена {self.ticker}: {price} USDT."
                }))
            except Exception as e:
                await self.send(text_data=json.dumps({
                    'message': f"Ошибка при получении цены: {str(e)}"
                }))
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        if 'ticker' in data:
            self.ticker = data['ticker']
            await self.send(text_data=json.dumps({
                'message': f"Вы выбрали тикер: {self.ticker}. Обновление цен начнётся."
            }))
        else:
            await self.send(text_data=json.dumps({
                'message': 'Ошибка: Укажите тикер.'
            }))
