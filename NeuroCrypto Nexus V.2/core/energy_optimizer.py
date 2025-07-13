import torch
import time


class EnergyEfficientTraining:
    """Оптимизация энергопотребления при обучении"""

    def __init__(self):
        self.energy_budget = 100
        self.current_energy = 0
        self.start_time = 0
        self.learning_rate_history = []

    def configure(self, model, max_energy=100, target_efficiency=0.85):
        self.model = model
        self.energy_budget = max_energy
        self.target_efficiency = target_efficiency
        self.current_energy = 0

    def start_training_session(self):
        self.start_time = time.time()
        self.current_energy = 0
        logging.info("Начало энергоэффективной сессии обучения")

    def step(self, loss_value):
        """Адаптивный шаг обучения с учетом энергии"""
        # Рассчет энергетической стоимости
        energy_cost = 0.1 + 0.01 * loss_value

        if self.current_energy + energy_cost > self.energy_budget:
            logging.warning("Превышен энергетический бюджет, остановка обучения")
            return False

        self.current_energy += energy_cost
        return True

    def adjust_learning_rate(self, optimizer, epoch, loss):
        """Адаптивная регулировка скорости обучения"""
        if len(self.learning_rate_history) > 10:
            avg_loss = sum(self.learning_rate_history[-10:]) / 10
            if loss > avg_loss * 1.1:
                for param_group in optimizer.param_groups:
                    param_group['lr'] *= 0.95
            elif loss < avg_loss * 0.9:
                for param_group in optimizer.param_groups:
                    param_group['lr'] *= 1.05

        self.learning_rate_history.append(loss)

    def end_training_session(self):
        duration = time.time() - self.start_time
        efficiency = (self.current_energy / duration) * 1000  # Условные единицы
        logging.info(f"Завершение сессии. Энергоэффективность: {efficiency:.2f} ед/сек")