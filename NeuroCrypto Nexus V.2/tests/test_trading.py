import unittest
from core.trading_bot import TradingBot
from interfaces.trading_api import TradingAPI


class TestTradingSystem(unittest.TestCase):

    def test_trade_execution(self):
        bot = TradingBot()
        balance_before = bot.get_account_balance("BTC")
        # Здесь будет тест выполнения торговой операции
        self.assertTrue(True)

    def test_api_connection(self):
        api = TradingAPI()
        balance = api.get_balance("BTC")
        self.assertIsInstance(balance, float)

    def test_risk_management(self):
        from core.risk_management import RiskManager
        manager = RiskManager()
        position_size = manager.calculate_position_size(10000, 0.01, 50000, 49000)
        self.assertAlmostEqual(position_size, 0.2, places=1)


if __name__ == '__main__':
    unittest.main()