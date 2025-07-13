import logging
from core.risk_management import RiskManager
from interfaces.trading_api import TradingAPI


class TradingBot:
    """Автономный торговый бот с нейроморфными алгоритмами"""

    def __init__(self, engine):
        self.engine = engine
        self.api = TradingAPI()
        self.risk_manager = RiskManager()
        self.logger = logging.getLogger("TradingBot")

    def execute_trade(self, symbol, signal, confidence):
        """Выполнение торговой операции на основе сигнала"""
        current_price = self.api.get_price(symbol)
        balance = self.api.get_balance("USDT")

        # Расчет размера позиции
        position_size = self.risk_manager.calculate_position_size(
            account_balance=balance,
            risk_per_trade=0.02,
            entry_price=current_price,
            stop_loss=current_price * 0.98
        )

        # Размещение ордера
        if signal == "BUY":
            self.api.place_order(symbol, "BUY", position_size)
            self.logger.info(f"🟢 BUY {position_size} {symbol} @ {current_price}")
        elif signal == "SELL":
            self.api.place_order(symbol, "SELL", position_size)
            self.logger.info(f"🔴 SELL {position_size} {symbol} @ {current_price}")

    def run_strategy(self):
        """Запуск торговой стратегии"""
        while True:
            # Получение данных и прогнозирование
            data = self.engine.fetch_data()
            prediction = self.engine.predict(data)

            # Принятие решения
            if prediction > 0.7:
                self.execute_trade("BTC/USDT", "BUY", prediction)
            elif prediction < 0.3:
                self.execute_trade("BTC/USDT", "SELL", 1 - prediction)

            # Пауза между итерациями
            time.sleep(60)