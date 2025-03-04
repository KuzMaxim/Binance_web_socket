import json
import aiohttp
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer  # type: ignore

class BinanceAPI:
    def __init__(self):
        self.base_url = "https://api.binance.com"

    async def fetch(self, relative_url, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + relative_url, params=params) as response:
                response.raise_for_status()
                return await response.json()

    async def get_coin(self, ticker: str) -> str:
        params = {"symbol": ticker}
        content = await self.fetch("/api/v3/ticker/price", params=params)
        return str(content["price"])

class TickerConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.binance_api = BinanceAPI()
        self.active = True
    
    async def connect(self):
        await self.accept()
        await self.send_initial_price()

        # Запускаем задачу для периодического обновления цены
        asyncio.create_task(self.send_periodic_updates("BTCUSDT"))

    async def disconnect(self):
        self.active = False

    async def send_initial_price(self):
        try:
            price = await self.binance_api.get_coin("BTCUSDT")
            await self.send(text_data=json.dumps({
                'message': f"Текущая цена Bitcoin (BTC) составляет {price} USDT."
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'message': f"Ошибка при получении цены Bitcoin: {str(e)}"
            }))

    async def send_periodic_updates(self, ticker: str):
        while self.active:
            await asyncio.sleep(10)  # Ждем 60 секунд
            try:
                price = await self.binance_api.get_coin(ticker)
                await self.send(text_data=json.dumps({
                    'message': f"Обновлённая цена Bitcoin (BTC): {price} USDT."
                }))
            except Exception as e:
                await self.send(text_data=json.dumps({
                    'message': f"Ошибка при получении цены Bitcoin: {str(e)}"
                }))
    
    async def receive(self, text_data):
        # Обработчик получения пользовательских сообщений
        pass
