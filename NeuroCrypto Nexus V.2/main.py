import os

# Установка переменных окружения для совместимости
os.environ["NPY_PROMOTION_STATE"] = "weak"
os.environ["NPY_USE_GETITEM"] = "1"
os.environ["NUMPY_EXPERIMENTAL_ARRAY_FUNCTION"] = "0"
os.environ["TORCHVISION_DISABLE_FBCODE"] = "1"
os.environ["USE_TORCHTRT"] = "0"  # Полное отключение проблемной библиотеки

import torch
import logging
from core.neural_engine import NeuralEngine
from interfaces.neuro_cli import NeuroCLI
from interfaces.dashboard import launch_trading_dashboard
from modules.self_healing.system_doctor import SystemDoctor
from modules.quantum_simulator import QuantumNoiseSimulator
from modules.federated_learning import FederatedLearningCoordinator

# Настройка прецизионных вычислений
torch.set_float32_matmul_precision('high')
torch.backends.cuda.matmul.allow_tf32 = True


def initialize_neuro_system():
    """Инициализация нейроморфной системы"""
    neuro_engine = NeuralEngine(
        device_map="auto",
        precision="fp16",
        neuromorphic_mode=True
    )
    SystemDoctor.health_check()
    NeuroCLI.activate_control_room()

    # Инициализация новых модулей
    QuantumNoiseSimulator.initialize()
    FederatedLearningCoordinator.setup()

    return neuro_engine


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s | %(levelname)s | %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger("NeuroCortex")
    logger.info("⚡ Запуск NeuroCrypto Nexus V.2")

    try:
        neuro_system = initialize_neuro_system()
        neuro_system.activate_autonomous_mode()

        # Запуск новой веб-панели
        launch_trading_dashboard()

    except Exception as e:
        SystemDoctor.critical_recovery(e)