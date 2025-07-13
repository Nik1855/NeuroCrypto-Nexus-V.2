import numpy as np
from sklearn.ensemble import IsolationForest
from pyod.models.auto_encoder import AutoEncoder
import logging


class AnomalyDetector:
    """Обнаружение аномалий в финансовых данных в реальном времени"""

    def __init__(self, model_type='autoencoder', contamination=0.01):
        self.model_type = model_type
        self.contamination = contamination
        self.model = self._init_model(model_type)
        self.logger = logging.getLogger("AnomalyDetector")

    def _init_model(self, model_type):
        """Инициализация модели обнаружения аномалий"""
        if model_type == 'isolation_forest':
            return IsolationForest(contamination=self.contamination)
        elif model_type == 'autoencoder':
            return AutoEncoder(contamination=self.contamination)
        else:
            raise ValueError(f"Неизвестный тип модели: {model_type}")

    def train(self, data):
        """Обучение модели на нормальных данных"""
        self.model.fit(data)
        self.logger.info("Модель обнаружения аномалий обучена")

    def detect(self, data_point):
        """Обнаружение аномалий в новой точке данных"""
        prediction = self.model.predict(data_point.reshape(1, -1))
        return prediction[0] == 1  # 1 = аномалия, 0 = норма

    def detect_batch(self, data_batch):
        """Пакетное обнаружение аномалий"""
        return self.model.predict(data_batch) == 1