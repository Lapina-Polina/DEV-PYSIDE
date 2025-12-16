import time
import requests
import psutil

from PySide6 import QtCore


class SystemInfo(QtCore.QThread):
    # сигнал, передающий список [cpu, ram]
    systemInfoReceived = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None

    def run(self) -> None:
        # если задержка не передана
        if self.delay is None:
            self.delay = 1

        # бесконечный цикл получения информации
        while True:
            # загрузка CPU
            cpu_value = psutil.cpu_percent()

            # загрузка RAM
            ram_value = psutil.virtual_memory().percent

            # передаём данные через сигнал
            self.systemInfoReceived.emit([cpu_value, ram_value])

            # пауза
            time.sleep(self.delay)


class WeatherHandler(QtCore.QThread):
    # сигналы
    weatherDataReceived = QtCore.Signal(dict)
    errorOccurred = QtCore.Signal(str)

    def __init__(self, lat, lon, parent=None):
        super().__init__(parent)

        self.__api_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}&current_weather=true"
        )
        self.__delay = 10
        self.__status = True

    def setDelay(self, delay) -> None:
        """
        Метод для установки времени задержки обновления сайта
        """
        self.__delay = delay

    def stop(self) -> None:
        self.__status = False

    def run(self) -> None:
        while self.__status:
            try:
                response = requests.get(self.__api_url, timeout=5)
                data = response.json()

                # передаём данные через сигнал
                self.weatherDataReceived.emit(data)

            except Exception as e:
                self.errorOccurred.emit(str(e))

            time.sleep(self.__delay)
