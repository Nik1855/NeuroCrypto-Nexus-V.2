import numpy as np
from sklearn.ensemble import IsolationForest
from pyod.models.auto_encoder import AutoEncoder


class AnomalyDetector:
    """Обнаружение аномалий в реальном времени"""

    def __init__(self, model_type='isolation_forest', contamination=0.01):
        self.model_type = model_type
        self.contamination = contamination
        self.models = {
            'isolation_forest': IsolationForest(contamination=contamination),
            'autoencoder': AutoEncoder(contamination=contamination)
        }
        self.model = self.models[model_type]
        self.is_trained = False

    def train(self, data):
        """Обучение модели на нормальных данных"""
        self.model.fit(data)
        self.is_trained = True
        return self

    def detect(self, data_point):
        """Обнаружение аномалий в новой точке данных"""
        if not self.is_trained:
            raise RuntimeError("Модель не обучена")

        prediction = self.model.predict(data_point.reshape(1, -1))
        return prediction[0] == 1  # 1 = аномалия, 0 = норма

    def realtime_monitoring(self, data_stream):
        """Потоковый мониторинг данных в реальном времени"""
        anomalies = []
        for point in data_stream:
            if self.detect(point):
                anomalies.append(point)
                self._trigger_alert(point)
        return anomalies

    def _trigger_alert(self, anomaly):
        logging.warning(f"Обнаружена аномалия: {anomaly}")
        # Интеграция с системой уведомлений
        from interfaces.alert_system import AlertSystem
        AlertSystem.send_alert(f"Финансовая аномалия: {str(anomaly)[:50]}")