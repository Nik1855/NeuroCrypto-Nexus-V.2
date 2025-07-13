import numpy as np
import torch
from qiskit import QuantumCircuit, Aer, execute
from qiskit.algorithms.optimizers import SPSA
from qiskit_machine_learning.neural_networks import SamplerQNN


class QuantumSampler:
    """Интеграция квантовых вычислений для сэмплирования данных"""

    def __init__(self, n_qubits=5):
        self.n_qubits = n_qubits
        self.backend = Aer.get_backend('qasm_simulator')

    def apply(self, data):
        """Применение квантового сэмплинга к данным"""
        if isinstance(data, torch.Tensor):
            data = data.numpy()

        qc = QuantumCircuit(self.n_qubits)

        # Кодирование данных в квантовое состояние
        for i in range(min(self.n_qubits, len(data))):
            qc.rx(data[i], i)

        # Добавление энтэнглемента
        qc.h(range(self.n_qubits))
        for i in range(self.n_qubits - 1):
            qc.cx(i, i + 1)

        # Измерение
        qc.measure_all()

        # Выполнение
        result = execute(qc, self.backend, shots=1024).result()
        counts = result.get_counts()

        # Преобразование результатов
        probs = np.zeros(2 ** self.n_qubits)
        for state, count in counts.items():
            probs[int(state, 2)] = count / 1024

        return torch.tensor(probs[:len(data)]).float()