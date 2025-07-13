import requests
import logging
from config import *


class TradingAPI:
    """Унифицированный API для взаимодействия с криптобиржами"""

    def __init__(self, exchange='binance'):
        self.exchange = exchange
        self.base_url = EXCHANGE_URLS[exchange]
        self.logger = logging.getLogger(f"TradingAPI-{exchange}")

    def place_order(self, symbol, side, quantity, order_type='market'):
        """Размещение ордера"""
        endpoint = f"{self.base_url}/order"
        payload = {
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'type': order_type
        }

        try:
            response = requests.post(endpoint, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Ошибка размещения ордера: {response.text}")
                return None
        except Exception as e:
            self.logger.critical(f"Критическая ошибка: {str(e)}")
            return None

    def get_balance(self, asset):
        """Получение баланса актива"""
        endpoint = f"{self.base_url}/balance/{asset}"
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                return response.json()['balance']
            else:
                self.logger.error(f"Ошибка получения баланса: {response.text}")
                return 0.0
        except Exception as e:
            self.logger.critical(f"Критическая ошибка: {str(e)}")
            return 0.0