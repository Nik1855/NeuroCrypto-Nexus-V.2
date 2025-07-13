import os
from cryptography.fernet import Fernet
import logging


class SecurityManager:
    """Управление шифрованием и безопасностью данных"""

    def __init__(self):
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)
        self.logger = logging.getLogger("SecurityManager")

    def _load_or_generate_key(self):
        """Загрузка или генерация ключа шифрования"""
        key_path = "secret.key"
        if os.path.exists(key_path):
            with open(key_path, "rb") as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, "wb") as key_file:
                key_file.write(key)
            return key

    def encrypt_data(self, data):
        """Шифрование данных"""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data)

    def decrypt_data(self, encrypted_data):
        """Дешифрование данных"""
        return self.cipher.decrypt(encrypted_data).decode()

    def secure_api_key(self, api_name, api_key):
        """Безопасное хранение API ключей"""
        encrypted_key = self.encrypt_data(api_key)
        # Здесь будет сохранение в безопасное хранилище
        self.logger.info(f"API ключ для {api_name} защищен")
        return encrypted_key