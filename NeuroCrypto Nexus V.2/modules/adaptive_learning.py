import torch
from torch.optim.lr_scheduler import _LRScheduler
import math


class AdaptiveLearningScheduler(_LRScheduler):
    """Адаптивный планировщик скорости обучения с нейроморфной регуляцией"""

    def __init__(self, optimizer, energy_budget, last_epoch=-1):
        self.energy_budget = energy_budget
        self.current_energy = 0
        super().__init__(optimizer, last_epoch)

    def get_lr(self):
        """Адаптивная регулировка скорости обучения"""
        if self.current_energy > self.energy_budget * 0.8:
            # Снижение скорости обучения при высоком энергопотреблении
            return [base_lr * 0.5 for base_lr in self.base_lrs]
        return self.base_lrs

    def update_energy(self, energy_consumption):
        """Обновление информации о потреблении энергии"""
        self.current_energy += energy_consumption