from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from widgets.lab3.b_systeminfo_widget import SystemInfoWindow
from widgets.lab3.c_weatherapi_widget import WeatherApiWindow
from widgets.lab3.d_many_widgets_and_threads import ManyWidgetsThreadsWindow


class MainWindowLab3(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа 3")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout(self)

        buttons = [
            ("Системная информация\n(QThread)", SystemInfoWindow),
            ("Погода\n(QThread + requests)", WeatherApiWindow),
            ("Все виджеты вместе\n(threads)", ManyWidgetsThreadsWindow),
        ]
        
        for text, window_class in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(
                lambda _, wc=window_class: self.open_window(wc)
            )
            layout.addWidget(btn)

    def open_window(self, window_class):
        window = window_class()
        window.show()
        # чтобы окно не закрылось сборщиком мусора
        setattr(self, f"_open_{window_class.__name__}", window)
