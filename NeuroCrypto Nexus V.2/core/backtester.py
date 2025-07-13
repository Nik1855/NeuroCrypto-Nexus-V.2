import pandas as pd
import numpy as np
import logging


class Backtester:
    """Система бэктестинга торговых стратегий"""

    def __init__(self, data, initial_capital=10000.0):
        self.data = data
        self.initial_capital = initial_capital
        self.logger = logging.getLogger("Backtester")

    def run_backtest(self, strategy_function):
        """Запуск бэктеста для стратегии"""
        signals = strategy_function(self.data)
        positions = signals * self.initial_capital
        portfolio = positions.diff()
        portfolio.iloc[0] = positions.iloc[0]
        cumulative = portfolio.cumsum()

        # Расчет метрик
        results = {
            'cumulative_returns': cumulative,
            'sharpe_ratio': self._calculate_sharpe(cumulative),
            'max_drawdown': self._calculate_max_drawdown(cumulative),
            'performance': cumulative.iloc[-1] / self.initial_capital
        }

        self.logger.info(f"Результаты бэктеста: Sharpe={results['sharpe_ratio']:.2f}, "
                         f"MaxDrawdown={results['max_drawdown']:.2%}")

        return results

    def _calculate_sharpe(self, returns, risk_free_rate=0.0):
        """Расчет коэффициента Шарпа"""
        excess_returns = returns - risk_free_rate
        return excess_returns.mean() / excess_returns.std()

    def _calculate_max_drawdown(self, cumulative_returns):
        """Расчет максимальной просадки"""
        peak = cumulative_returns.expanding(min_periods=1).max()
        drawdown = (cumulative_returns - peak) / peak
        return drawdown.min()