import numpy as np
import torch
from qiskit import QuantumCircuit, Aer, execute
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error


class QuantumNoiseSimulator:
    """Симуляция квантовых шумов для финансовых данных"""

    def __init__(self, noise_level=0.05):
        self.noise_level = noise_level
        self.backend = Aer.get_backend('qasm_simulator')

    def apply_quantum_noise(self, data):
        """Применение квантового шума к данным"""
        circuit = QuantumCircuit(5)

        # Кодирование данных в квантовое состояние
        for i in range(min(5, len(data))):
            if data[i] > 0:
                circuit.rx(data[i], i)

        # Создание модели шума
        noise_model = NoiseModel()
        error = depolarizing_error(self.noise_level, 1)
        noise_model.add_all_qubit_quantum_error(error, ['rx'])

        # Измерение
        circuit.measure_all()

        # Выполнение с шумом
        result = execute(circuit, self.backend,
                         noise_model=noise_model,
                         shots=1024).result()
        counts = result.get_counts()

        # Преобразование результатов
        noisy_data = [int(bit) for bit in max(counts, key=counts.get)]
        return torch.tensor(noisy_data[:len(data)]).float()