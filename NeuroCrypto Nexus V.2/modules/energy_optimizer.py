import time
import logging


class EnergyEfficientTraining:
    """Оптимизация энергопотребления при обучении нейросетей"""

    def __init__(self, max_energy=100, target_efficiency=0.85):
        self.max_energy = max_energy
        self.target_efficiency = target_efficiency
        self.current_energy = 0
        self.learning_rate_history = []
        self.logger = logging.getLogger("EnergyOptimizer")

    def start_training_session(self):
        """Начало сессии обучения"""
        self.start_time = time.time()
        self.current_energy = 0
        self.logger.info("Начало энергоэффективной сессии обучения")

    def step(self, loss_value):
        """Адаптивный шаг обучения с учетом энергии"""
        energy_cost = 0.1 + 0.01 * loss_value

        if self.current_energy + energy_cost > self.max_energy:
            self.logger.warning("Превышен энергетический бюджет, остановка обучения")
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
        """Завершение сессии обучения"""
        duration = time.time() - self.start_time
        efficiency = (self.current_energy / duration) * 1000
        self.logger.info(f"Завершение сессии. Энергоэффективность: {efficiency:.2f} ед/сек")
        return efficiency >= self.target_efficiency