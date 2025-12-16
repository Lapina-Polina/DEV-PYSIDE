from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from widgets.lab1.login import LoginWindow  # Окно для Логина
from widgets.lab1.b_login import BLoginWindow  # Окно для Б-Логина
from widgets.lab1.ship_parameters import ShipParametersUI  # Параметры корабля
from widgets.lab1.engine_settings import EngineControlUI  # Управление двигателями
from widgets.lab1.profile_card import ProfileCardWindow  # Профиль
from widgets.lab1.book_shop import BookShopWindow  # Книжный магазин
from widgets.lab1.calculator import CalculatorWindow  # Калькулятор
from widgets.lab1.window import MainWindow  # Основное окно


class MainWindowLab1(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа 1")
        self.setGeometry(100, 100, 300, 400)

        layout = QVBoxLayout()

        buttons = [
            ("Логин", LoginWindow),
            ("Логин (В)", BLoginWindow),
            ("Основное окно", MainWindow),
            ("Параметры корабля", ShipParametersUI),
            ("Управление основными двигателями", EngineControlUI),
            ("Профиль", ProfileCardWindow),
            ("Книжный магазин", BookShopWindow),
            ("Калькулятор", CalculatorWindow),
        ]

        for text, window_class in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda _, wc=window_class: self.open_window(wc))  # Передаем класс окна
            layout.addWidget(btn)

        self.setLayout(layout)

    def open_window(self, window_class):
        # Открываем выбранное окно
        window = window_class()
        window.show()
        setattr(self, f"_open_{window_class.__name__}", window)
