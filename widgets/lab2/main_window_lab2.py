from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from widgets.lab2.a_create_ui import Window
from widgets.lab2.b_add_signals import AddWindow
from widgets.lab2.c_signals_events import SignalWindow
from widgets.lab2.d_eventfilter_settings import EventFilterSettings



class MainWindowLab2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа 2")
        self.setGeometry(100, 100, 300, 250)

        layout = QVBoxLayout()

        buttons = [
            ("Создание пользовательского интерфейса", Window),  # задания 1(a)
            ("Добавление сигналов", AddWindow),  # задания 2(b)
            ("Проверка состояния окна", SignalWindow),  # задание 3(c)
            ("Взаимодействия виджетов друг с другом", EventFilterSettings),  # задание 4(d)
        ]

        for text, window_class in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda _, wc=window_class: self.open_window(wc))
            layout.addWidget(btn)

        self.setLayout(layout)

    def open_window(self, window_class):
        window = window_class()
        window.show()
        setattr(self, f"_open_{window_class.__name__}", window)
