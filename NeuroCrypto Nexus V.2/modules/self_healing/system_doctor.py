import logging
import psutil
import numpy as np
import torch
from ..interfaces.alert_system import send_alert


class SystemDoctor:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logger = logging.getLogger("SystemDoctor")
        return cls._instance

    @staticmethod
    def health_check():
        """Комплексная проверка здоровья системы"""
        status = {
            "gpu_available": torch.cuda.is_available(),
            "gpu_memory": torch.cuda.mem_get_info()[1] / (1024 ** 3) if torch.cuda.is_available() else 0,
            "ram_usage": psutil.virtual_memory().percent,
            "numpy_version": np.__version__,
            "torch_version": torch.__version__
        }

        if not status["gpu_available"]:
            send_alert("Внимание: GPU недоступен, производительность снижена")

        if status["ram_usage"] > 90:
            send_alert(f"Критическое использование RAM: {status['ram_usage']}%")

        logging.info(f"Системный статус: {status}")
        return status

    @staticmethod
    def critical_recovery(error):
        """Процедура восстановления после критической ошибки"""
        logging.critical(f"⛑️ Критическая ошибка: {error}")

        # Автоматическое восстановление
        try:
            logging.info("Попытка автоматического восстановления...")
            torch.cuda.empty_cache()

            # Перезагрузка критических компонентов
            from core.neural_engine import NeuralEngine
            NeuralEngine.reload()

            logging.info("Восстановление завершено успешно")
            send_alert(f"Система восстановлена после ошибки: {str(error)[:100]}")
        except Exception as recovery_error:
            logging.critical(f"Ошибка восстановления: {recovery_error}")
            send_alert(f"Требуется ручное вмешательство: {str(recovery_error)[:100]}")
            raise recovery_error

    @staticmethod
    def resource_monitor():
        """Мониторинг ресурсов в реальном времени"""
        while True:
            cpu_usage = psutil.cpu_percent()
            gpu_usage = torch.cuda.utilization() if torch.cuda.is_available() else 0

            if cpu_usage > 90 or gpu_usage > 95:
                send_alert(f"Высокая нагрузка: CPU={cpu_usage}%, GPU={gpu_usage}%")

            # Проверка каждые 5 минут
            time.sleep(300)