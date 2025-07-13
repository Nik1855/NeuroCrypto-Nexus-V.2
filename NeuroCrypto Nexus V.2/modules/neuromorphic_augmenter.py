import torch
import numpy as np


class NeuromorphicAugmenter:
    """Нейроморфное усиление данных для финансовых временных рядов"""

    def __init__(self, noise_level=0.05):
        self.noise_level = noise_level

    def apply_spike_noise(self, data):
        """Добавление спайковых шумов, характерных для нейроморфных систем"""
        spike_indices = np.random.choice(len(data), size=int(len(data) * 0.1), replace=False)
        data[spike_indices] += torch.randn(len(spike_indices)) * self.noise_level * 5
        return data

    def apply_temporal_jitter(self, data, max_shift=3):
        """Добавление временного дрожания"""
        shift = torch.randint(-max_shift, max_shift, (1,)).item()
        return torch.roll(data, shift)

    def augment(self, data):
        """Применение всех методов усиления"""
        data = self.apply_spike_noise(data)
        data = self.apply_temporal_jitter(data)
        return data