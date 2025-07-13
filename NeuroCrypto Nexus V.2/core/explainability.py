import shap
import numpy as np
import matplotlib.pyplot as plt
import logging


class ExplainableAIModule:
    """Модуль объяснимого ИИ для интерпретации прогнозов"""

    def __init__(self, model, background_data):
        self.model = model
        self.explainer = shap.DeepExplainer(model, background_data)
        self.logger = logging.getLogger("ExplainableAI")

    def explain_prediction(self, input_data):
        """Генерация объяснения для конкретного прогноза"""
        shap_values = self.explainer.shap_values(input_data)
        return self._visualize_explanation(shap_values, input_data)

    def _visualize_explanation(self, shap_values, input_data):
        """Визуализация SHAP значений"""
        fig, ax = plt.subplots(figsize=(12, 6))
        shap.summary_plot(shap_values, input_data, show=False)
        plt.tight_layout()
        return fig

    def generate_feature_importance(self, dataset):
        """Генерация важности признаков для всего набора данных"""
        shap_values = self.explainer.shap_values(dataset)
        return np.abs(shap_values).mean(axis=0)