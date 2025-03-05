import json
import time
import websocket
from .models import Crypto

def save_crypto(ticker, price):
    crypto = Crypto(ticker=ticker, price=int(float(price)))
    crypto.full_clean()
    crypto.save()

def on_message(ws, message):
    json_data = json.loads(message)
    price = json_data['p']
    quantity = json_data['q']
    print(f"BTC/USDT - Цена: {price}, Количество: {quantity}")
    save_crypto(ticker="BTC", price=price)
    time.sleep(5)

def on_error(ws, error):
    print(f"Ошибка: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Соединение закрыто. Пробую переподключиться...")
    time.sleep(5)
    run()

def on_open(ws):
    print("Соединение открыто")

def run():
    btc_uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    
    websocket.enableTrace(True)  # Для отладки
    ws = websocket.WebSocketApp(btc_uri,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.on_open = on_open
    while True:
        try:
            ws.run_forever()
        except Exception as e:
            print(f"Ошибка при попытке подключения: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run()
