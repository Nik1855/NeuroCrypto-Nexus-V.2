import numpy as np


class RiskManager:
    """Управление рисками для торговых операций"""

    @staticmethod
    def calculate_position_size(account_balance, risk_per_trade, entry_price, stop_loss):
        """Расчет размера позиции на основе риска"""
        risk_amount = account_balance * risk_per_trade
        risk_per_unit = abs(entry_price - stop_loss)
        return risk_amount / risk_per_unit

    @staticmethod
    def calculate_dynamic_stop_loss(price_history, volatility_factor=2.0):
        """Динамический расчет стоп-лосса на основе волатильности"""
        volatility = np.std(price_history)
        return volatility * volatility_factor

    @staticmethod
    def calculate_profit_target(entry_price, stop_loss, risk_reward_ratio=3.0):
        """Расчет цели по прибыли на основе соотношения риск/вознаграждение"""
        risk = abs(entry_price - stop_loss)
        if entry_price > stop_loss:  # Long position
            return entry_price + risk * risk_reward_ratio
        else:  # Short position
            return entry_price - risk * risk_reward_ratio