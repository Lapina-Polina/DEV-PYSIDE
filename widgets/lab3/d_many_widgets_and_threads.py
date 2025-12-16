from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from widgets.lab3.b_systeminfo_widget import SystemInfoWindow
from widgets.lab3.c_weatherapi_widget import WeatherApiWindow


class ManyWidgetsThreadsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Все виджеты вместе")
        self.setGeometry(150, 150, 500, 600)

        layout = QVBoxLayout()

        title = QLabel("Системная информация и погода")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        title.setAlignment(
            title.alignment() | title.alignment().__class__.AlignCenter
        )

        # создаём предыдущие виджеты
        self.system_info_widget = SystemInfoWindow()
        self.weather_widget = WeatherApiWindow()

        layout.addWidget(title)
        layout.addWidget(self.system_info_widget)
        layout.addWidget(self.weather_widget)

        self.setLayout(layout)
