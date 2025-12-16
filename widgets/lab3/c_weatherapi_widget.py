from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, \
    QLabel, QLineEdit, QPushButton, QSpinBox
from PySide6.QtCore import Qt

from widgets.lab3.a_threads import WeatherHandler


class WeatherApiWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Weather API")
        self.setGeometry(200, 200, 360, 300)

        # UI
        main_layout = QVBoxLayout()

        # координаты
        coord_layout = QHBoxLayout()

        self.lat_input = QLineEdit()
        self.lat_input.setPlaceholderText("Широта")

        self.lon_input = QLineEdit()
        self.lon_input.setPlaceholderText("Долгота")

        coord_layout.addWidget(self.lat_input)
        coord_layout.addWidget(self.lon_input)

        # задержка
        delay_layout = QHBoxLayout()
        delay_label = QLabel("Задержка (сек):")

        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(5, 60)
        self.delay_spin.setValue(10)

        delay_layout.addWidget(delay_label)
        delay_layout.addWidget(self.delay_spin)

        # кнопка управления
        self.control_btn = QPushButton("Запустить")

        # вывод погоды
        self.weather_label = QLabel("Информация о погоде появится здесь")
        self.weather_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_label.setWordWrap(True)

        main_layout.addLayout(coord_layout)
        main_layout.addLayout(delay_layout)
        main_layout.addWidget(self.control_btn)
        main_layout.addWidget(self.weather_label)

        self.setLayout(main_layout)

        # THREAD
        self.thread = None

        # SIGNALS
        self.control_btn.clicked.connect(self.toggle_thread)

    def toggle_thread(self):
        """Запуск / остановка потока"""
        if self.thread is None or not self.thread.isRunning():
            self.start_thread()
        else:
            self.stop_thread()

    def start_thread(self):
        # проверка координат
        try:
            lat = float(self.lat_input.text())
            lon = float(self.lon_input.text())
        except ValueError:
            self.weather_label.setText("Введите корректные широту и долготу")
            return

        # блокируем поля
        self.lat_input.setDisabled(True)
        self.lon_input.setDisabled(True)
        self.delay_spin.setDisabled(True)

        # создаём и настраиваем поток
        self.thread = WeatherHandler(lat, lon)
        self.thread.setDelay(self.delay_spin.value())

        self.thread.weatherDataReceived.connect(self.update_weather)
        self.thread.errorOccurred.connect(self.show_error)

        self.thread.start()

        self.control_btn.setText("Остановить")

    def stop_thread(self):
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait()

        # разблокируем поля
        self.lat_input.setDisabled(False)
        self.lon_input.setDisabled(False)
        self.delay_spin.setDisabled(False)

        self.control_btn.setText("Запустить")

    def update_weather(self, data: dict):
        """Отображение данных о погоде"""
        current = data.get("current_weather", {})
        temperature = current.get("temperature", "—")
        windspeed = current.get("windspeed", "—")

        self.weather_label.setText(
            f"Температура: {temperature} °C\n"
            f"Скорость ветра: {windspeed} м/с"
        )

    def show_error(self, message: str):
        self.weather_label.setText(f"Ошибка: {message}")

    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait()
        event.accept()
