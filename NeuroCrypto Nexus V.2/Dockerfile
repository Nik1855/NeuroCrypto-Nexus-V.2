FROM nvidia/cuda:12.1.1-base

# Установка Python
RUN apt-get update && apt-get install -y python3.11 python3-pip

# Создание рабочей директории
WORKDIR /app

# Копирование файлов проекта
COPY . .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Установка специфичных зависимостей PyG
RUN pip install --no-cache-dir \
    pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv \
    -f https://data.pyg.org/whl/torch-2.3.0+cu121.html

# Настройка переменных окружения
ENV NPY_PROMOTION_STATE="weak"
ENV NPY_USE_GETITEM="1"
ENV NUMPY_EXPERIMENTAL_ARRAY_FUNCTION="0"
ENV TORCHVISION_DISABLE_FBCODE="1"
ENV USE_TORCHTRT="0"

# Команда запуска
CMD ["python", "main.py"]