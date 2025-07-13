import requests
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


class AlertSystem:
    """Система уведомлений через Telegram"""

    @staticmethod
    def send_alert(message):
        """Отправка предупреждения в Telegram"""
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"🚨 NeuroCrypto Alert: {message}",
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                logging.info(f"Alert sent: {message}")
            else:
                logging.error(f"Failed to send alert: {response.text}")
        except Exception as e:
            logging.critical(f"Alert system failure: {str(e)}")

    @staticmethod
    def send_trading_signal(signal, asset, confidence):
        """Отправка торгового сигнала"""
        emoji = "📈" if signal == "BUY" else "📉" if signal == "SELL" else "⚠️"
        message = (
            f"{emoji} Торговый сигнал: {signal}\n"
            f"Актив: {asset}\n"
            f"Уверенность: {confidence:.2%}\n"
            f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        AlertSystem.send_alert(message)