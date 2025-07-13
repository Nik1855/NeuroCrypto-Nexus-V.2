import speech_recognition as sr
import pyttsx3
import logging


class VoiceInterface:
    """Голосовой интерфейс для взаимодействия с системой"""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.logger = logging.getLogger("VoiceInterface")

    def listen(self):
        """Прослушивание голосовых команд"""
        with sr.Microphone() as source:
            self.logger.info("Слушаю...")
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language='ru-RU')
            self.logger.info(f"Распознано: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Ошибка распознавания: {str(e)}")
            return ""

    def speak(self, text):
        """Озвучивание ответа"""
        self.engine.say(text)
        self.engine.runAndWait()
        self.logger.info(f"Озвучено: {text}")