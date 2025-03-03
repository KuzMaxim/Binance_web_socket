import requests

class BinanceAPI:
    def __init__(self):
        self.base_url = "https://api.binance.com"

    def fetch(self, relative_url, params=None):
        response = requests.get(self.base_url + relative_url, params=params)
        response.raise_for_status()
        return response.json()

    def get_coin(self, ticker: str) -> str:
        params = {"symbol": ticker}
        content = self.fetch("/api/v3/ticker/price", params=params)
        return str(content["price"])