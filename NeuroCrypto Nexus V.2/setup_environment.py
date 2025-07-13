import os
import subprocess
import sys
import logging


def setup_environment():
    """Автоматическая настройка окружения для NeuroCrypto Nexus V.2"""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Проверка и установка необходимого ПО
    required_packages = [
        "torch==2.3.0",
        "torchvision==0.18.0",
        "torchaudio==2.3.0",
        "torch-geometric==2.6.1",
        "numpy==1.26.4"
    ]

    logging.info("🔧 Начало настройки NeuroCrypto Nexus V.2")

    # Создание виртуального окружения
    if not os.path.exists(".venv"):
        logging.info("Создание виртуального окружения...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)

    # Активация окружения (Windows)
    if sys.platform == "win32":
        activate_script = os.path.join(".venv", "Scripts", "activate")
    else:
        activate_script = os.path.join(".venv", "bin", "activate")

    # Установка пакетов
    logging.info("Установка зависимостей...")
    install_cmd = [
                      os.path.join(".venv", "Scripts" if sys.platform == "win32" else "bin", "pip"),
                      "install",
                      "--no-cache-dir"
                  ] + required_packages

    subprocess.run(install_cmd, check=True)

    # Установка специфических зависимостей для PyG
    pyg_cmd = install_cmd + [
        "pyg_lib",
        "torch_scatter",
        "torch_sparse",
        "torch_cluster",
        "torch_spline_conv",
        "-f",
        "https://data.pyg.org/whl/torch-2.3.0+cu121.html"
    ]
    subprocess.run(pyg_cmd, check=True)

    logging.info("✅ Настройка окружения завершена успешно!")
    logging.info("Активируйте окружение и запустите: python main.py")


if __name__ == "__main__":
    setup_environment()