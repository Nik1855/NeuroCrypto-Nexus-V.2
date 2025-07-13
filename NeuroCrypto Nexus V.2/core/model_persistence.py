import torch
import joblib
import os
import logging


class ModelPersistence:
    """Управление сохранением и загрузкой моделей"""

    def __init__(self, model_dir="saved_models"):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        self.logger = logging.getLogger("ModelPersistence")

    def save_model(self, model, model_name, version="1.0"):
        """Сохранение модели в файл"""
        path = os.path.join(self.model_dir, f"{model_name}_v{version}.pt")
        if isinstance(model, torch.nn.Module):
            torch.save(model.state_dict(), path)
        else:
            joblib.dump(model, path.replace('.pt', '.pkl'))
        self.logger.info(f"Модель {model_name} сохранена в {path}")
        return path

    def load_model(self, model_name, version="1.0", model_class=None):
        """Загрузка модели из файла"""
        path = os.path.join(self.model_dir, f"{model_name}_v{version}.pt")
        if model_class and issubclass(model_class, torch.nn.Module):
            model = model_class()
            model.load_state_dict(torch.load(path))
            model.eval()
            return model
        else:
            return joblib.load(path.replace('.pt', '.pkl'))