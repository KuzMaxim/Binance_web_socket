import json
import time
import websocket
from .models import Crypto
import asyncio

# Список пар валют для подписки
symbols = ["btcusdt", "ethusdt", "ltcusdt", "btceur", "etheur", "ltceur", "btcrub", "ethrub"]
subscribed_symbols = ','.join([f"{symbol}@trade" for symbol in symbols])

def on_message(ws, message):
    json_string = message.replace("'", '"')

    # Преобразование строки JSON в словарь
    try:
        json_data = json.loads(json_string)
        print(type(json_data))
        print(json_data)  # Для отладки - выводим полученные данные

        price = json_data['p']
        quantity = json_data['q']
        ticker = json_data['s']

        print(f"{ticker} - Цена: {price}, Количество: {quantity}")
        asyncio.run(Crypto.post(ticker=str(ticker).encode('utf-8'), price=float(price)))
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
    except Exception as e:
        print(f"Общая ошибка: {e}")


def on_error(ws, error):
    print(f"Ошибка: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Соединение закрыто. Пробую переподключиться...")
    print(close_status_code)
    print(close_msg)
    #time.sleep(5)
    ws.run_forever()

def on_open(ws):
    print("Соединение открыто, подписываюсь на торги...")
    request = {
        "method": "SUBSCRIBE",
        "params": subscribed_symbols.split(','),
        "id": 1
    }
    ws.send(json.dumps(request))


def run():
    websocket_url = "wss://stream.binance.com:9443/ws"
    ws = websocket.WebSocketApp(websocket_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()

run()
