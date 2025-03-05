import json
import time
import websocket
import threading
from .models import Crypto

def save_crypto(ticker, price):
    crypto = Crypto(ticker=ticker, price=int(float(price)))
    crypto.full_clean()
    crypto.save()

def on_message(ws, message):
    json_data = json.loads(message)
    price = json_data['p']
    quantity = json_data['q']
   
    ticker = json_data['s']
    print(f"{ticker} - Цена: {price}, Количество: {quantity}")
    save_crypto(ticker=ticker, price=price)
    time.sleep(15)

def on_error(ws, error):
    print(f"Ошибка: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Соединение закрыто. Пробую переподключиться...")
    time.sleep(5)


def on_open(ws, ticker):
    print(f"Соединение открыто для {ticker}")
    request = {
        "method": "SUBSCRIBE",
        "params": [
            f"{ticker}@trade"
        ],
        "id": 1
    }
    ws.send(json.dumps(request))

def run_ticker(ticker):
    websocket_url = "wss://stream.binance.com:9443/ws"
    ws = websocket.WebSocketApp(websocket_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)


    ws.on_open = lambda ws: on_open(ws, ticker)
    ws.run_forever()

def run():
    crypto_currencies = ["btc", "eth", "ltc"]
    currencies = ["usdt", "eur", "rub"]

    for crypto_currency in crypto_currencies:
        for currency in currencies:
            t = threading.Thread(target=run_ticker, args=(crypto_currency+currency,))
            t.start()
            time.sleep(0.5)
